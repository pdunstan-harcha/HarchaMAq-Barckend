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
        usuario=nombre_display
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
        """Listar recargas con paginación y búsqueda - SIN joins complejos, usando lazy loading"""
        
        # Query base SIN joinedload para evitar problemas
        query = SARecarga.query
        
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

        ultimo = SARecarga.query.order_by(SARecarga.pkRecarga.desc()).first()
        siguiente_num = (ultimo.pkRecarga if ultimo else 0) + 1
        codigo = f"RCO{str(siguiente_num).zfill(8)}"
        
        print(f"🔵 Creando recarga con código: {codigo}")
        print(f"🔵 Payload: {payload}")
        
        # Convertir 0 a None para campos opcionales
        def safe_int(value):
            if value == 0 or value == "0" or value is None:
                return None
            return int(value) if value else None
        
        try:
            rec = SARecarga(
                ID_RECARGA=codigo,
                ID_MAQUINA=payload.get("ID_MAQUINA"),
                pkMaquina=payload.get("pkMaquina"),
                USUARIO_ID=payload.get("USUARIO_ID"),
                pkUsuario=payload.get("pkUsuario"),
                FECHA=payload.get("FECHA") if payload.get("FECHA") else datetime.datetime.now().date(),
                FECHAHORA_RECARGA=payload.get("FECHAHORA_RECARGA") if payload.get("FECHAHORA_RECARGA") else datetime.datetime.now(),
                LITROS=payload.get("LITROS"),
                FOTO=payload.get("FOTO"),
                Observaciones=payload.get("OBSERVACIONES"),
                ODOMETRO=payload.get("ODOMETRO"),
                KILOMETROS=payload.get("KILOMETROS"),
                PATENTE=payload.get("PATENTE") if payload.get("PATENTE") != "string" else None,
                
                # Manejar campos opcionales - convertir 0 a None
                pkOperador=safe_int(payload.get("pkOperador")),
                ID_OPERADOR=payload.get("ID_OPERADOR"),
                RUT_OPERADOR=payload.get("RUT_OPERADOR") if payload.get("RUT_OPERADOR") != "string" else None,
                pkObra=safe_int(payload.get("pkObra")),
                pkCliente=safe_int(payload.get("pkCliente")),
                OBRA_ID=payload.get("OBRA_ID"),
                CLIENTE_ID=payload.get("CLIENTE_ID"),
            )
            
            print(f"🔵 Objeto SARecarga creado")
            
            db.session.add(rec)
            print(f"🔵 Agregado a sesión")
            
            db.session.commit()
            print(f"🔵 Commit realizado")
            
            db.session.refresh(rec)
            print(f"🔵 Refresh realizado, pkRecarga: {rec.pkRecarga}")
            
            result = _to_domain(rec, include_relations=False)
            print(f"🔵 Convertido a dominio: {result}")
            
            return result
            
        except Exception as e:
            print(f"❌ ERROR en crear(): {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            raise
    
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