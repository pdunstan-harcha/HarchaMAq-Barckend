import datetime
from typing import Sequence, Optional
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, func
from app.models import (
    RecargaCombustible as SARecarga, 
    Maquina as SAMaquina, 
    User as SAUser, 
    Obra as SAObra, 
    Cliente as SACliente
)
from app import db
from ..domain.entity import Recarga
from ..domain.refs import MaquinaRef, UsuarioRef, ObraRef, ClienteRef
from ..domain.repository import RecargaRepository, PaginationParams, PaginatedResult

def _maq_ref(maq: Optional[SAMaquina]) -> Optional[MaquinaRef]:
    if not maq:
        return None
    return MaquinaRef(
        id=maq.pkMaquina, 
        nombre=maq.MAQUINA or f"Máquina {maq.pkMaquina}"
    )

def _user_ref(user: Optional[SAUser]) -> Optional[UsuarioRef]:
    if not user:
        return None

    # Usar múltiples campos como fallback
    nombre_display = (
        user.NOMBREUSUARIO or
        user.USUARIO or
        (f"{user.NOMBRE or ''} {user.APELLIDOS or ''}".strip()) or
        user.USUARIO_ID or
        f"Usuario {user.pkUsuario}"
    )

    return UsuarioRef(
        id=user.pkUsuario,
        usuario=nombre_display,
        # ✅ NUEVO - Incluir todos los campos del usuario
        usuario_id=user.USUARIO_ID,
        nombre=user.NOMBRE,
        apellidos=user.APELLIDOS,
        rol=user.ROL,
        email=getattr(user, 'EmailUsuario', None),
        telefono=user.TELEFONO,
        rut=user.RUT
    )

def _obra_ref(obra: Optional[SAObra]) -> Optional[ObraRef]:
    if not obra:
        return None
    return ObraRef(
        id=obra.pkObra, 
        nombre=obra.OBRA or f"Obra {obra.pkObra}"
    )

def _cliente_ref(cliente: Optional[SACliente]) -> Optional[ClienteRef]:
    if not cliente:
        return None
    return ClienteRef(
        id=cliente.pkCliente, 
        nombre=cliente.CLIENTE or f"Cliente {cliente.pkCliente}"
    )

def _to_domain(recarga: SARecarga, include_relations: bool = True) -> Recarga:
    """Convertir SQLAlchemy a dominio - SIN recursión infinita"""
    return Recarga(
        id=recarga.pkRecarga,
        codigo=recarga.ID_RECARGA,
        fecha=recarga.FECHA,
        litros=recarga.LITROS,
        foto=recarga.FOTO,
        observaciones=recarga.Observaciones,
        odometro=recarga.ODOMETRO,
        kilometros=recarga.KILOMETROS,
        fechahora_recarga=recarga.FECHAHORA_RECARGA,
        patente=recarga.PATENTE,
        rut_operador=recarga.RUT_OPERADOR,
        id_recarga_anterior=recarga.ID_Recarga_Anterior,
        litros_anterior=recarga.Litros_Anterior,
        horometro_anterior=recarga.Horometro_Anterior,
        kilometro_anterior=recarga.Kilometro_Anterior,
        fecha_anterior=recarga.Fecha_Anterior,
        
        # Referencias - SOLO si include_relations=True
        maquina=_maq_ref(recarga.maquina) if include_relations else None,
        usuario=_user_ref(recarga.usuario) if include_relations else None,
        operador=_user_ref(recarga.operador) if include_relations else None,
        obra=_obra_ref(recarga.obra) if include_relations else None,
        cliente=_cliente_ref(recarga.cliente) if include_relations else None,
        
        # ❌ ELIMINAR recursión infinita - solo referencia básica
        recarga_anterior=None,  # Por ahora eliminamos para evitar recursión
        usuario_ultima_modificacion=_user_ref(recarga.usuario_ultima_modificacion) if include_relations else None
    )

class SqlAlchemyRecargaRepository(RecargaRepository):
    
    def listar_paginado(self, params: PaginationParams) -> PaginatedResult:
        """Listar recargas con paginación y búsqueda - CON joins para cargar relaciones"""

        # ✅ Query base CON joinedload para cargar todas las relaciones
        query = SARecarga.query.options(
            joinedload(SARecarga.maquina),
            joinedload(SARecarga.usuario),
            joinedload(SARecarga.operador),
            joinedload(SARecarga.obra),      
            joinedload(SARecarga.cliente),
            joinedload(SARecarga.usuario_ultima_modificacion)
        )
        
        
        # Aplicar filtro de usuario si existe (para roles PETROLERO/OPERADOR)
        if params.user_filter:
            print(f"🔵 REPO RECARGAS - Aplicando filtro usuario: {params.user_filter}")
            query = query.filter(SARecarga.pkUsuario == params.user_filter)
        else:
            print(f"🔵 REPO RECARGAS - Sin filtro de usuario")
        
        # Aplicar búsqueda si existe - SIMPLIFICADA
        if params.search:
            search_term = f"%{params.search}%"
            query = query.filter(
                or_(
                    SARecarga.ID_RECARGA.ilike(search_term),
                    SARecarga.PATENTE.ilike(search_term),
                    SARecarga.RUT_OPERADOR.ilike(search_term),
                    SARecarga.Observaciones.ilike(search_term)
                )
            )
        
        # Contar total ANTES de paginar
        total = query.count()
        
        # Aplicar ordenamiento y paginación
        items = (
            query
            .order_by(SARecarga.FECHAHORA_RECARGA.desc())
            .offset((params.page - 1) * params.per_page)
            .limit(params.per_page)
            .all()
        )
        
        # Convertir a dominio CON relaciones incluidas
        recargas_domain = [_to_domain(recarga, include_relations=True) for recarga in items]
        
        return PaginatedResult(
            data=recargas_domain,
            total=total,
            page=params.page,
            per_page=params.per_page
        )
    
    def obtener_por_id(self, recarga_id: int) -> Optional[Recarga]:
        """Obtener una recarga específica por ID - usando lazy loading"""
        recarga = SARecarga.query.filter(SARecarga.pkRecarga == recarga_id).first()
        return _to_domain(recarga, include_relations=True) if recarga else None
    
    def crear(self, payload: dict) -> Recarga:
        """Crear nueva recarga"""
        try:
            codigo = self._generar_codigo()
            print(f"🔵 Creando recarga con código: {codigo}")
            print(f"🔵 Payload recibido: {payload}")

            pk_obra, pk_cliente, pk_operador = self._extraer_ids(payload)
            print("🔵 IDs procesados:")
            print(f"  - pkObra: {pk_obra}")
            print(f"  - pkCliente: {pk_cliente}")
            print(f"  - pkOperador: {pk_operador}")

            rec = self._crear_objeto_recarga(payload, codigo, pk_obra, pk_cliente, pk_operador)
            print("🔵 Objeto SARecarga creado con:")
            print(f"  - pkObra: {rec.pkObra}")
            print(f"  - pkCliente: {rec.pkCliente}")

            db.session.add(rec)
            db.session.commit()
            db.session.refresh(rec)
            print(f"🔵 Commit y refresh realizado, pkRecarga: {rec.pkRecarga}")

            # ✅ NUEVO - Actualizar tabla MAQUINAS con datos de esta recarga como última recarga
            self._actualizar_maquina_ultima_recarga(rec)

            rec_with_relations = self._recargar_con_relaciones(rec.pkRecarga)
            self._imprimir_relaciones(rec_with_relations)

            result = _to_domain(rec_with_relations, include_relations=True)
            print("🔵 Convertido a dominio con relaciones")
            return result

        except Exception as e:
            print(f"❌ ERROR en crear(): {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            raise

    def _generar_codigo(self) -> str:
        ultimo = SARecarga.query.order_by(SARecarga.pkRecarga.desc()).first()
        siguiente_num = (ultimo.pkRecarga if ultimo else 0) + 1
        return f"RCO{str(siguiente_num).zfill(8)}"

    def _safe_int(self, value):
        """Convertir a int de forma segura, permitiendo 0 como valor válido"""
        if value is None or value == "":
            return None
        try:
            parsed = int(value)
            # ✅ Retornar None solo si es el string "0", pero permitir el integer 0
            if parsed == 0 and isinstance(value, str):
                return None
            return parsed
        except (ValueError, TypeError):
            return None

    def _safe_str(self, value):
        if value is None or value == "" or value == "string":
            return None
        return str(value).strip()

    def _extraer_ids(self, payload):
        pk_obra = self._safe_int(payload.get("pkObra") or payload.get("OBRA_ID") or payload.get("OBRA"))
        pk_cliente = self._safe_int(payload.get("pkCliente") or payload.get("CLIENTE_ID") or payload.get("CLIENTE"))
        pk_operador = self._safe_int(payload.get("pkOperador") or payload.get("OPERADOR_ID"))
        return pk_obra, pk_cliente, pk_operador

    def _crear_objeto_recarga(self, payload, codigo, pk_obra, pk_cliente, pk_operador):
        return SARecarga(
            ID_RECARGA=codigo,
            ID_MAQUINA=payload.get("ID_MAQUINA"),
            pkMaquina=payload.get("pkMaquina"),
            USUARIO_ID=payload.get("USUARIO_ID"),
            pkUsuario=payload.get("pkUsuario"),
            FECHA=payload.get("FECHA") if payload.get("FECHA") else datetime.datetime.now().date(),
            FECHAHORA_RECARGA=payload.get("FECHAHORA_RECARGA") if payload.get("FECHAHORA_RECARGA") else datetime.datetime.now(),
            LITROS=payload.get("LITROS"),
            FOTO=self._safe_str(payload.get("FOTO")),
            Observaciones=self._safe_str(payload.get("OBSERVACIONES")),
            ODOMETRO=self._safe_int(payload.get("ODOMETRO")),
            KILOMETROS=self._safe_int(payload.get("KILOMETROS")),
            PATENTE=self._safe_str(payload.get("PATENTE")),
            pkOperador=pk_operador,
            ID_OPERADOR=payload.get("ID_OPERADOR"),
            RUT_OPERADOR=self._safe_str(payload.get("RUT_OPERADOR")),
            pkObra=pk_obra,
            pkCliente=pk_cliente,
            OBRA_ID=str(pk_obra) if pk_obra else None,
            CLIENTE_ID=str(pk_cliente) if pk_cliente else None,

            # ✅ NUEVO - Datos de recarga anterior (historial)
            pkRecarga_anterior=self._safe_int(payload.get("pkRecarga_anterior")),
            ID_Recarga_Anterior=self._safe_str(payload.get("ID_Recarga_Anterior")),
            Litros_Anterior=self._safe_int(payload.get("Litros_Anterior")),
            Horometro_Anterior=self._safe_int(payload.get("Horometro_Anterior")),
            Kilometro_Anterior=self._safe_int(payload.get("Kilometro_Anterior")),
            Fecha_Anterior=payload.get("Fecha_Anterior"),
        )

    def _actualizar_maquina_ultima_recarga(self, recarga: SARecarga):
        """Actualizar la tabla MAQUINAS con los datos de la última recarga"""
        try:
            maquina = SAMaquina.query.get(recarga.pkMaquina)
            if not maquina:
                print(f"⚠️ Máquina {recarga.pkMaquina} no encontrada para actualizar")
                return

            # Actualizar campos de última recarga en la tabla MAQUINAS
            maquina.HR_Actual = recarga.ODOMETRO  # Horómetro actual
            maquina.KM_Actual = recarga.KILOMETROS  # Kilómetros actuales
            maquina.pkUltima_recarga = recarga.pkRecarga  # ID de esta recarga
            maquina.ID_Ultima_Recarga = recarga.ID_RECARGA  # Código de esta recarga
            maquina.Litros_Ultima = recarga.LITROS  # Litros de esta recarga
            maquina.Fecha_Ultima = recarga.FECHAHORA_RECARGA  # Fecha de esta recarga

            db.session.commit()
            print(f"✅ Máquina {maquina.pkMaquina} actualizada con última recarga {recarga.pkRecarga}")
            print(f"   - HR_Actual: {maquina.HR_Actual}")
            print(f"   - KM_Actual: {maquina.KM_Actual}")
            print(f"   - Litros_Ultima: {maquina.Litros_Ultima}")

        except Exception as e:
            print(f"❌ ERROR al actualizar máquina: {str(e)}")
            db.session.rollback()

    def _recargar_con_relaciones(self, pk_recarga):
        return (
            SARecarga.query
            .options(
                joinedload(SARecarga.maquina),
                joinedload(SARecarga.usuario),
                joinedload(SARecarga.operador),
                joinedload(SARecarga.obra),
                joinedload(SARecarga.cliente),
                joinedload(SARecarga.usuario_ultima_modificacion)
            )
            .filter(SARecarga.pkRecarga == pk_recarga)
            .first()
        )

    def _imprimir_relaciones(self, rec_with_relations):
        print(f"🔵 Recarga recargada con relaciones:")
        print(f"  - Tiene obra: {rec_with_relations.obra is not None}")
        print(f"  - Tiene cliente: {rec_with_relations.cliente is not None}")
        if rec_with_relations.obra:
            print(f"  - Obra nombre: {rec_with_relations.obra.OBRA}")
        if rec_with_relations.cliente:
            print(f"  - Cliente nombre: {rec_with_relations.cliente.CLIENTE}")
    
    def actualizar(self, recarga_id: int, payload: dict) -> Optional[Recarga]:
        """Actualizar una recarga existente"""
        print(f"🔵 Actualizando recarga {recarga_id}")
        print(f"🔵 Payload de actualización: {payload}")
        
        try:
            recarga = (
                SARecarga.query
                .filter(SARecarga.pkRecarga == recarga_id)
                .first()
            )
            
            if not recarga:
                print(f"❌ Recarga {recarga_id} no encontrada")
                return None
            
            print(f"🔵 Recarga encontrada: {recarga.ID_RECARGA}")
            
            # Convertir 0 a None para campos opcionales
            def safe_int(value):
                if value == 0 or value == "0" or value is None:
                    return None
                return int(value) if value else None
            
            def clean_string(value):
                if value == "string" or value == "" or value is None:
                    return None
                return str(value).strip()
            
            # Actualizar campos permitidos
            campos_actualizables = {
                'LITROS': lambda x: int(x) if x is not None else None,
                'FOTO': clean_string,
                'Observaciones': clean_string,  # Nota: campo con mayúscula
                'ODOMETRO': lambda x: int(x) if x is not None else None,
                'KILOMETROS': lambda x: int(x) if x is not None else None,
                'PATENTE': clean_string,
                'pkOperador': safe_int,
                'ID_OPERADOR': clean_string,
                'RUT_OPERADOR': clean_string,
                'pkObra': safe_int,
                'pkCliente': safe_int,
                'OBRA_ID': clean_string,
                'CLIENTE_ID': clean_string,
                # Campos adicionales que pueden actualizarse
                'pkMaquina': safe_int,
                'ID_MAQUINA': clean_string,
                'pkUsuario': safe_int,
                'USUARIO_ID': clean_string
            }
            
            updated_fields = []
            for campo, transform_func in campos_actualizables.items():
                if campo in payload:
                    old_value = getattr(recarga, campo, None)
                    new_value = transform_func(payload[campo])
                    
                    if old_value != new_value:
                        setattr(recarga, campo, new_value)
                        updated_fields.append(f"{campo}: {old_value} -> {new_value}")
                        print(f"🔵 Actualizando {campo}: {old_value} -> {new_value}")
            
            if not updated_fields:
                print("⚠️ No hay campos para actualizar")
                return _to_domain(recarga, include_relations=False)
            
            print(f"🔵 Campos actualizados: {', '.join(updated_fields)}")
            
            # Actualizar fecha de última modificación
            import datetime
            recarga.USUARIO_ID_UltimaModificacion = payload.get('usuario_modificacion')
            recarga.pkUsuario_UltimaModificacion = payload.get('pk_usuario_modificacion')
            
            db.session.commit()
            print(f"🔵 Commit realizado")
            
            db.session.refresh(recarga)
            print(f"🔵 Refresh realizado")
            
            result = _to_domain(recarga, include_relations=False)
            print(f"🔵 Convertido a dominio")
            
            return result
            
        except Exception as e:
            print(f"❌ ERROR en actualizar(): {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            raise
    
    def eliminar(self, recarga_id: int) -> bool:
        """Eliminar una recarga"""
        print(f"🔵 Eliminando recarga {recarga_id}")
        
        try:
            recarga = (
                SARecarga.query
                .filter(SARecarga.pkRecarga == recarga_id)
                .first()
            )
            
            if not recarga:
                print(f"❌ Recarga {recarga_id} no encontrada para eliminar")
                return False
            
            print(f"🔵 Recarga encontrada: {recarga.ID_RECARGA}")
            
            # Verificar si hay dependencias (recargas que referencian a esta como anterior)
            dependencias = (
                SARecarga.query
                .filter(SARecarga.pkRecarga_anterior == recarga_id)
                .count()
            )
            
            if dependencias > 0:
                print(f"⚠️ No se puede eliminar: {dependencias} recargas dependen de esta")
                raise ValueError(f"No se puede eliminar: {dependencias} recargas posteriores dependen de esta recarga")
            
            db.session.delete(recarga)
            print(f"🔵 Marcado para eliminar")
            
            db.session.commit()
            print(f"🔵 Eliminación confirmada")
            
            return True
            
        except ValueError:
            # Re-lanzar errores de validación
            db.session.rollback()
            raise
        except Exception as e:
            print(f"❌ ERROR en eliminar(): {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            raise