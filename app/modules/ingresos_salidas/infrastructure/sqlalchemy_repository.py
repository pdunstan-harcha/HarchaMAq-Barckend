import datetime
from typing import Sequence, Optional
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, func, desc
from app.models import (
    MaquinaIngresoSalida as SAIngresoSalida,
    Maquina as SAMaquina, 
    User as SAUser
)
from app import db
from ..domain.entity import IngresoSalida
from ..domain.refs import MaquinaRef, UsuarioRef
from ..domain.repository import IngresoSalidaRepository, PaginationParams, PaginatedResult

def _maq_ref(maq: Optional[SAMaquina]) -> Optional[MaquinaRef]:
    if not maq:
        return None
    return MaquinaRef(
        id=maq.pkMaquina, 
        nombre=maq.MAQUINA or f"Máquina {maq.pkMaquina}",
        codigo=maq.CODIGO_MAQUINA
    )

def _user_ref(user: Optional[SAUser]) -> Optional[UsuarioRef]:
    if not user:
        return None
    nombre_completo = f"{user.NOMBRE or ''} {user.APELLIDOS or ''}".strip()
    return UsuarioRef(
        id=user.pkUsuario, 
        usuario=user.NOMBREUSUARIO or f"Usuario {user.pkUsuario}",
        nombre_completo=nombre_completo if nombre_completo else None
    )

def _format_tiempo(tiempo_obj):
    """Formatear tiempo a string legible"""
    if not tiempo_obj:
        return None
    
    # Si es un objeto time
    if hasattr(tiempo_obj, 'hour'):
        hours = tiempo_obj.hour
        minutes = tiempo_obj.minute
        seconds = tiempo_obj.second
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    # Si es string, devolverlo tal como está
    return str(tiempo_obj)

def _create_movimiento_anterior_texto(ultimo_is, maquina_nombre):
    """Crear texto descriptivo del movimiento anterior"""
    if not ultimo_is:
        return "Sin movimiento anterior registrado"
    
    tipo = ultimo_is.INGRESO_SALIDA or "Movimiento"
    fecha = ultimo_is.FECHAHORA.strftime("%d/%m/%y %H:%M") if ultimo_is.FECHAHORA else "Sin fecha"
    estado = ultimo_is.ESTADO_MAQUINA or "Sin estado"
    
    return f"{tipo} - {fecha} -> {estado}"

def _to_domain(is_record: SAIngresoSalida, include_relations: bool = True) -> IngresoSalida:
    """Convertir SQLAlchemy a dominio - Con campos adicionales del formulario"""
    
    # Obtener información de relaciones si es necesario
    maquina_ref = _maq_ref(is_record.maquina) if include_relations and is_record.maquina else None
    usuario_ref = _user_ref(is_record.usuario) if include_relations and is_record.usuario else None
    
    # Crear texto del movimiento anterior
    movimiento_anterior_texto = None
    if is_record.ingreso_salida_anterior:
        maquina_nombre = maquina_ref.nombre if maquina_ref else "Máquina desconocida"
        movimiento_anterior_texto = _create_movimiento_anterior_texto(
            is_record.ingreso_salida_anterior, 
            maquina_nombre
        )
    
    # Formatear tiempo
    tiempo_formateado = _format_tiempo(is_record.TIEMPO)
    
    return IngresoSalida(
        id=is_record.pkIs,
        codigo=is_record.ID_IS,
        id_maquina=is_record.ID_MAQUINA,
        fechahora=is_record.FECHAHORA,
        ingreso_salida=is_record.INGRESO_SALIDA,
        id_ultimo_is=is_record.ID_ULTIMO_IS,
        fechahora_ultimo=is_record.FECHAHORA_ULTIMO,
        tiempo=is_record.TIEMPO,
        estado_maquina=is_record.ESTADO_MAQUINA,
        control1=is_record.Control1,
        observaciones=is_record.Observaciones,
        editar_fecha=is_record.Editar_Fecha,
        fecha_editada=is_record.Fecha_Editada,
        usuario_id=is_record.USUARIO_ID,
        
        # ✅ CAMPOS ADICIONALES
        movimiento_anterior_texto=movimiento_anterior_texto,
        puede_modificar_fecha=is_record.Editar_Fecha == "SI",
        tiempo_formateado=tiempo_formateado,
        
        # Referencias
        maquina=maquina_ref,
        usuario=usuario_ref,
        ingreso_salida_anterior=None  # Evitar recursión
    )

class SqlAlchemyIngresoSalidaRepository(IngresoSalidaRepository):
    
    # ✅ NUEVO MÉTODO: Obtener máquinas con su último movimiento
    def obtener_maquinas_con_ultimo_movimiento(self):
        """Obtener todas las máquinas con información de su último movimiento"""
        from app.models import Maquina as SAMaquina
        
        maquinas = SAMaquina.query.all()
        resultado = []
        
        for maquina in maquinas:
            ultimo_is = self.obtener_ultimo_por_maquina(maquina.pkMaquina)
            
            # Determinar qué movimientos son válidos
            puede_ingresar = True
            puede_salir = True
            ultimo_movimiento_texto = "Sin registros"
            
            if ultimo_is:
                ultimo_movimiento_texto = f"{ultimo_is.ingreso_salida} - {ultimo_is.fechahora.strftime('%d/%m/%y %H:%M') if ultimo_is.fechahora else 'Sin fecha'} -> {ultimo_is.estado_maquina or 'Sin estado'}"
                
                # Lógica de validación: no pueden ser consecutivos del mismo tipo
                if ultimo_is.ingreso_salida == "INGRESO":
                    puede_ingresar = False  # No puede ingresar si el último fue ingreso
                elif ultimo_is.ingreso_salida == "SALIDA":
                    puede_salir = False     # No puede salir si el último fue salida
            
            resultado.append({
                'id': maquina.pkMaquina,
                'nombre': f"[{maquina.CODIGO_MAQUINA or f'M{maquina.pkMaquina:02d}'}] - {maquina.MAQUINA or f'Máquina {maquina.pkMaquina}'}",
                'codigo': maquina.CODIGO_MAQUINA,
                'ultimo_movimiento': ultimo_movimiento_texto,
                'puede_ingresar': puede_ingresar,
                'puede_salir': puede_salir
            })
        
        return resultado
    
    def listar_paginado(self, params: PaginationParams) -> PaginatedResult:
        """Listar ingresos/salidas con paginación y búsqueda"""
        
        # Query base con joins opcionales
        query = SAIngresoSalida.query
        
        # Aplicar búsqueda si existe
        if params.search:
            search_term = f"%{params.search}%"
            query = query.filter(
                or_(
                    SAIngresoSalida.ID_IS.ilike(search_term),
                    SAIngresoSalida.ID_MAQUINA.ilike(search_term),
                    SAIngresoSalida.INGRESO_SALIDA.ilike(search_term),
                    SAIngresoSalida.ESTADO_MAQUINA.ilike(search_term),
                    SAIngresoSalida.Observaciones.ilike(search_term),
                    SAIngresoSalida.USUARIO_ID.ilike(search_term)
                )
            )
        
        # Contar total ANTES de paginar
        total = query.count()
        
        # Aplicar ordenamiento y paginación
        items = (
            query
            .order_by(desc(SAIngresoSalida.FECHAHORA))
            .offset((params.page - 1) * params.per_page)
            .limit(params.per_page)
            .all()
        )
        
        # Convertir a dominio SIN relaciones complejas
        ingresos_salidas_domain = [_to_domain(is_record, include_relations=False) for is_record in items]
        
        return PaginatedResult(
            data=ingresos_salidas_domain,
            total=total,
            page=params.page,
            per_page=params.per_page
        )
    
    def obtener_por_id(self, ingreso_salida_id: int) -> Optional[IngresoSalida]:
        """Obtener un ingreso/salida específico por ID"""
        is_record = (
            SAIngresoSalida.query
            .filter(SAIngresoSalida.pkIs == ingreso_salida_id)
            .first()
        )
        
        return _to_domain(is_record, include_relations=False) if is_record else None
    
    def obtener_ultimo_por_maquina(self, maquina_id: int) -> Optional[IngresoSalida]:
        """Obtener el último ingreso/salida de una máquina específica"""
        is_record = (
            SAIngresoSalida.query
            .filter(SAIngresoSalida.pkMaquina == maquina_id)
            .order_by(desc(SAIngresoSalida.FECHAHORA))
            .first()
        )
        
        return _to_domain(is_record, include_relations=False) if is_record else None
    
    def crear(self, payload: dict) -> IngresoSalida:
        """Crear nuevo ingreso/salida - Con validaciones mejoradas"""
        now = datetime.datetime.now()
        
        # Usar fecha personalizada si se proporciona
        fechahora_movimiento = payload.get("FECHAHORA")
        if fechahora_movimiento:
            if isinstance(fechahora_movimiento, str):
                try:
                    # Intentar parsear diferentes formatos
                    formatos = [
                        "%Y-%m-%d %H:%M:%S",
                        "%d-%m-%Y %H:%M:%S", 
                        "%Y-%m-%dT%H:%M:%S",
                        "%Y-%m-%d %H:%M"
                    ]
                    for formato in formatos:
                        try:
                            fechahora_movimiento = datetime.datetime.strptime(fechahora_movimiento, formato)
                            break
                        except ValueError:
                            continue
                    else:
                        # Si no se puede parsear, usar la actual
                        fechahora_movimiento = now
                except:
                    fechahora_movimiento = now
        else:
            fechahora_movimiento = now
        
        # ✅ GENERAR CÓDIGO CORTO
        codigo = f"IS{now.strftime('%y%m%d%H%M%S')}"
        
        print(f"🔵 Creando {payload.get('INGRESO_SALIDA')} con código: {codigo}")
        print(f"🔵 Fecha/Hora: {fechahora_movimiento}")
        
        # Obtener último movimiento para validaciones
        maquina_id = payload.get('pkMaquina')
        ultimo_is = None
        tiempo_calculado = None
        
        if maquina_id:
            ultimo_is = self.obtener_ultimo_por_maquina(maquina_id)
            
            # Calcular tiempo entre movimientos
            if ultimo_is and ultimo_is.fechahora:
                delta = fechahora_movimiento - ultimo_is.fechahora
                total_seconds = int(delta.total_seconds())
                
                if total_seconds >= 0:  # Solo si la nueva fecha es posterior
                    days = delta.days
                    hours = (total_seconds % 86400) // 3600
                    minutes = (total_seconds % 3600) // 60
                    seconds = total_seconds % 60
                    
                    # Si hay días, convertir a horas adicionales
                    total_hours = hours + (days * 24)
                    
                    # Limitar a 23:59:59 para el campo TIME de MySQL
                    if total_hours > 23:
                        total_hours = 23
                        minutes = 59
                        seconds = 59
                    
                    tiempo_calculado = datetime.time(
                        hour=total_hours,
                        minute=minutes,
                        second=seconds
                    )
        
        try:
            is_record = SAIngresoSalida(
                ID_IS=codigo,
                ID_MAQUINA=payload.get("ID_MAQUINA"),
                pkMaquina=payload.get("pkMaquina"),
                FECHAHORA=fechahora_movimiento,
                INGRESO_SALIDA=payload.get("INGRESO_SALIDA"),
                
                # Información del registro anterior
                ID_ULTIMO_IS=ultimo_is.codigo if ultimo_is else None,
                pkUltimo_is=ultimo_is.id if ultimo_is else None,
                FECHAHORA_ULTIMO=ultimo_is.fechahora if ultimo_is else None,
                TIEMPO=tiempo_calculado,
                
                ESTADO_MAQUINA=payload.get("ESTADO_MAQUINA", "OPERATIVA"),
                Control1=payload.get("Control1"),
                Observaciones=payload.get("Observaciones"),
                Editar_Fecha=payload.get("editar_fecha", "NO"),
                Fecha_Editada=None,
                USUARIO_ID=payload.get("USUARIO_ID"),
                pkUsuario=payload.get("pkUsuario")
            )
            
            db.session.add(is_record)
            db.session.commit()
            db.session.refresh(is_record)
            
            print(f"✅ {payload.get('INGRESO_SALIDA')} creado exitosamente - ID: {is_record.pkIs}")
            
            return _to_domain(is_record, include_relations=False)
            
        except Exception as e:
            print(f"❌ ERROR en crear(): {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            raise
    
    def actualizar(self, ingreso_salida_id: int, payload: dict) -> Optional[IngresoSalida]:
        """Actualizar un ingreso/salida existente"""
        print(f"🔵 Actualizando ingreso/salida {ingreso_salida_id}")
        
        try:
            is_record = (
                SAIngresoSalida.query
                .filter(SAIngresoSalida.pkIs == ingreso_salida_id)
                .first()
            )
            
            if not is_record:
                print(f"❌ Ingreso/Salida {ingreso_salida_id} no encontrado")
                return None
            
            # Campos actualizables
            campos_actualizables = {
                'INGRESO_SALIDA': str,
                'ESTADO_MAQUINA': str,
                'Observaciones': str,
                'Control1': int
            }
            
            updated_fields = []
            for campo, tipo in campos_actualizables.items():
                if campo in payload:
                    old_value = getattr(is_record, campo, None)
                    new_value = payload[campo]
                    
                    if new_value is not None and new_value != "":
                        if tipo == int:
                            new_value = int(new_value)
                        else:
                            new_value = str(new_value)
                    else:
                        new_value = None
                    
                    if old_value != new_value:
                        setattr(is_record, campo, new_value)
                        updated_fields.append(f"{campo}: {old_value} -> {new_value}")
            
            # Marcar como editado
            if updated_fields:
                is_record.Editar_Fecha = "SI"
                is_record.Fecha_Editada = datetime.datetime.now()
                
                print(f"🔵 Campos actualizados: {', '.join(updated_fields)}")
                
                db.session.commit()
                db.session.refresh(is_record)
            
            return _to_domain(is_record, include_relations=False)
            
        except Exception as e:
            print(f"❌ ERROR en actualizar(): {str(e)}")
            db.session.rollback()
            raise
    
    def eliminar(self, ingreso_salida_id: int) -> bool:
        """Eliminar un ingreso/salida"""
        print(f"🔵 Eliminando ingreso/salida {ingreso_salida_id}")
        
        try:
            is_record = (
                SAIngresoSalida.query
                .filter(SAIngresoSalida.pkIs == ingreso_salida_id)
                .first()
            )
            
            if not is_record:
                return False
            
            # Verificar dependencias
            dependencias = (
                SAIngresoSalida.query
                .filter(SAIngresoSalida.pkUltimo_is == ingreso_salida_id)
                .count()
            )
            
            if dependencias > 0:
                raise ValueError(f"No se puede eliminar: {dependencias} registros posteriores dependen de este")
            
            db.session.delete(is_record)
            db.session.commit()
            
            print(f"🔵 Ingreso/Salida {ingreso_salida_id} eliminado exitosamente")
            return True
            
        except ValueError:
            db.session.rollback()
            raise
        except Exception as e:
            print(f"❌ ERROR en eliminar(): {str(e)}")
            db.session.rollback()
            raise