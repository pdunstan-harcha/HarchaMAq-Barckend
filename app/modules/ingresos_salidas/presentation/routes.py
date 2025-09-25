from flask_restx import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.security.roles import roles_required, ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_INSPECTOR
from .schemas import (
    ingresos_salidas_ns,
    ingreso_salida_input,
    ingresos_salidas_list_response,
    create_ingreso_salida_response,
    ingreso_salida_detail_response,
    maquinas_disponibles_response,  # ✅ AHORA SÍ EXISTE
    error_response
)

# Importar la arquitectura DDD
from ..infrastructure.sqlalchemy_repository import SqlAlchemyIngresoSalidaRepository
from ..application.listar import ListIngresosSalidasUseCase, ListIngresosSalidasInput
from ..application.obtener import GetIngresoSalidaUseCase, GetIngresoSalidaInput
from ..application.crear import CreateIngresoSalidaUseCase, CreateIngresoSalidaInput
from ..application.actualizar import UpdateIngresoSalidaUseCase, UpdateIngresoSalidaInput
from ..application.eliminar import DeleteIngresoSalidaUseCase, DeleteIngresoSalidaInput
from ..domain.entity import IngresoSalida

# Instanciar repositorio y casos de uso
ingresos_salidas_repository = SqlAlchemyIngresoSalidaRepository()
list_ingresos_salidas_use_case = ListIngresosSalidasUseCase(repo=ingresos_salidas_repository)
get_ingreso_salida_use_case = GetIngresoSalidaUseCase(repo=ingresos_salidas_repository)
create_ingreso_salida_use_case = CreateIngresoSalidaUseCase(repo=ingresos_salidas_repository)
update_ingreso_salida_use_case = UpdateIngresoSalidaUseCase(repo=ingresos_salidas_repository)
delete_ingreso_salida_use_case = DeleteIngresoSalidaUseCase(repo=ingresos_salidas_repository)

def _domain_to_dict(is_record: IngresoSalida) -> dict:
    """Convertir entidad de dominio a diccionario para API - Formato según CSV original"""
    
    # Debug logging
    print(f"🔍 DEBUG _domain_to_dict:")
    print(f"  - is_record.usuario_id: {is_record.usuario_id} (type: {type(is_record.usuario_id)})")
    print(f"  - is_record.usuario: {is_record.usuario}")
    if is_record.usuario:
        print(f"  - is_record.usuario.id: {is_record.usuario.id} (type: {type(is_record.usuario.id)})")
        print(f"  - is_record.usuario.usuario: {is_record.usuario.usuario}")
    
    return {
        # Datos principales del CSV: pkIs, ID_IS, ID_MAQUINA, pkMaquina, FECHAHORA, INGRESO_SALIDA, etc.
        'id': is_record.id,                                          # pkIs
        'codigo': is_record.codigo,                                  # ID_IS
        'fechahora': is_record.fechahora.isoformat() if is_record.fechahora else None,  # FECHAHORA
        'ingreso_salida': is_record.ingreso_salida,                  # INGRESO_SALIDA  
        'tiempo': str(is_record.tiempo) if is_record.tiempo else None,              # TIEMPO
        'tiempo_formateado': is_record.tiempo_formateado,            # Tiempo legible
        'fechahora_ultimo': is_record.fechahora_ultimo.isoformat() if is_record.fechahora_ultimo else None,  # FECHAHORA_ULTIMO
        'estado_maquina': is_record.estado_maquina,                  # ESTADO_MAQUINA (NUEVO ESTADO)
        'observaciones': is_record.observaciones,                    # OBSERVACIONES
        'usuario_id': is_record.usuario.id if is_record.usuario else None,  # Usar pkUsuario en lugar de USUARIO_ID
        
        # Información de la máquina (con JOIN)
        'maquina_id': is_record.maquina.id if is_record.maquina else None,           # pkMaquina
        'maquina': is_record.maquina.nombre if is_record.maquina else None,          # MAQUINA (nombre completo)
        'maquina_codigo': is_record.maquina.codigo if is_record.maquina else None,   # Para referencia
        
        # Usuario
        'usuario_nombre': is_record.usuario.usuario if is_record.usuario else None,  # Nombre del usuario
        
        # Campos adicionales útiles para el frontend
        'editar_fecha': is_record.editar_fecha,
        'fecha_editada': is_record.fecha_editada.isoformat() if is_record.fecha_editada else None,
        'puede_modificar_fecha': is_record.puede_modificar_fecha,
        'movimiento_anterior_texto': is_record.movimiento_anterior_texto
    }

# ✅ ENDPOINT DE MÁQUINAS DISPONIBLES - Ahora con el modelo correcto
@ingresos_salidas_ns.route('/maquinas-disponibles')
class MaquinasDisponibles(Resource):
    
    @ingresos_salidas_ns.marshal_with(maquinas_disponibles_response)
    @ingresos_salidas_ns.response(200, 'Lista de máquinas con estado de movimientos')
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_INSPECTOR])
    def get(self):
        """Obtener lista de máquinas con información de último movimiento para el dropdown"""
        try:
            print("🔵 GET /ingresos-salidas/maquinas-disponibles")
            
            maquinas_info = ingresos_salidas_repository.obtener_maquinas_con_ultimo_movimiento()
            
            print(f"🔵 {len(maquinas_info)} máquinas encontradas")
            
            return {
                'success': True,
                'data': maquinas_info
            }
        except Exception as e:
            print(f"❌ ERROR al obtener máquinas disponibles: {str(e)}")
            import traceback
            traceback.print_exc()
            ingresos_salidas_ns.abort(500, error=str(e))

@ingresos_salidas_ns.route('/')
class IngresosSalidasList(Resource):
    
    @ingresos_salidas_ns.doc(params={
        'page': 'Número de página (default: 1)',
        'per_page': 'Registros por página (10-100, default: 20)',
        'search': 'Búsqueda en código, máquina, tipo, estado u observaciones'
    })
    @ingresos_salidas_ns.marshal_with(ingresos_salidas_list_response)
    @ingresos_salidas_ns.response(200, 'Lista de ingresos/salidas obtenida')
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_INSPECTOR])
    def get(self):
        """Obtener lista paginada de ingresos y salidas de máquinas"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            search = request.args.get('search', '', type=str)
            
            input_data = ListIngresosSalidasInput(
                page=page,
                per_page=per_page,
                search=search if search else None
            )
            
            result = list_ingresos_salidas_use_case.execute(input_data)
            
            ingresos_salidas_data = [_domain_to_dict(is_rec) for is_rec in result.data]
            
            print(f"🔵 {len(ingresos_salidas_data)} registros encontrados (página {page})")
            
            return {
                'success': True,
                'data': ingresos_salidas_data,
                'pagination': {
                    'total': result.total,
                    'page': result.page,
                    'per_page': result.per_page,
                    'total_pages': result.total_pages,
                    'has_next': result.has_next,
                    'has_prev': result.has_prev
                }
            }
        except Exception as e:
            print(f"❌ ERROR en ingresos-salidas: {str(e)}")
            import traceback
            traceback.print_exc()
            ingresos_salidas_ns.abort(500, error=str(e))

    @ingresos_salidas_ns.expect(ingreso_salida_input, validate=True)
    @ingresos_salidas_ns.marshal_with(create_ingreso_salida_response)
    @ingresos_salidas_ns.response(201, 'Ingreso/Salida creado exitosamente')
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN])
    def post(self):
        """Crear un nuevo ingreso o salida de máquina"""
        try:
            print("🔵 POST /ingresos-salidas/")
            
            data = request.get_json()
            print(f"🔵 Data recibida: {data}")
            
            # Validación básica
            if not data:
                ingresos_salidas_ns.abort(400, error="No se recibieron datos")
            
            # Verificar campos requeridos
            required_fields = ['pkMaquina', 'pkUsuario', 'INGRESO_SALIDA']
            for field in required_fields:
                if field not in data or data[field] is None:
                    ingresos_salidas_ns.abort(400, error=f"Campo requerido: {field}")
            
            input_data = CreateIngresoSalidaInput(payload=data)
            result = create_ingreso_salida_use_case.execute(input_data)
            
            return {
                'success': True,
                'data': _domain_to_dict(result),
                'message': f'{result.ingreso_salida} registrado exitosamente'
            }, 201
            
        except ValueError as e:
            print(f"❌ ValueError: {str(e)}")
            ingresos_salidas_ns.abort(400, error=str(e))
        except Exception as e:
            print(f"❌ ERROR al crear ingreso/salida: {str(e)}")
            import traceback
            traceback.print_exc()
            ingresos_salidas_ns.abort(500, error=str(e))

@ingresos_salidas_ns.route('/<int:ingreso_salida_id>')
class IngresosSalidasDetail(Resource):
    
    @ingresos_salidas_ns.marshal_with(ingreso_salida_detail_response)
    @ingresos_salidas_ns.response(200, 'Ingreso/Salida obtenido exitosamente')
    @ingresos_salidas_ns.response(404, 'Ingreso/Salida no encontrado')
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_INSPECTOR])
    def get(self, ingreso_salida_id):
        """Obtener un ingreso/salida específico por ID"""
        try:
            print(f"🔵 GET /ingresos-salidas/{ingreso_salida_id}")
            
            input_data = GetIngresoSalidaInput(ingreso_salida_id=ingreso_salida_id)
            result = get_ingreso_salida_use_case.execute(input_data)
            
            if not result.found:
                print(f"❌ Ingreso/Salida {ingreso_salida_id} no encontrado")
                ingresos_salidas_ns.abort(404, error=f"Ingreso/Salida {ingreso_salida_id} no encontrado")
            
            print(f"✅ Ingreso/Salida {ingreso_salida_id} encontrado")
            
            return {
                'success': True,
                'data': _domain_to_dict(result.data)
            }
        except Exception as e:
            print(f"❌ ERROR al obtener ingreso/salida {ingreso_salida_id}: {str(e)}")
            ingresos_salidas_ns.abort(500, error=str(e))

    @ingresos_salidas_ns.expect(ingreso_salida_input, validate=False)
    @ingresos_salidas_ns.marshal_with(ingreso_salida_detail_response)
    @ingresos_salidas_ns.response(200, 'Ingreso/Salida actualizado exitosamente')
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN])
    def put(self, ingreso_salida_id):
        """Actualizar un ingreso/salida"""
        try:
            print(f"🔵 PUT /ingresos-salidas/{ingreso_salida_id}")
            
            data = request.get_json()
            if not data:
                ingresos_salidas_ns.abort(400, error="No se recibieron datos para actualizar")
            
            input_data = UpdateIngresoSalidaInput(ingreso_salida_id=ingreso_salida_id, payload=data)
            result = update_ingreso_salida_use_case.execute(input_data)
            
            if not result.updated:
                if "no encontrado" in result.message:
                    ingresos_salidas_ns.abort(404, error=result.message)
                else:
                    ingresos_salidas_ns.abort(400, error=result.message)
            
            return {
                'success': True,
                'data': _domain_to_dict(result.data),
                'message': result.message
            }
        except ValueError as e:
            print(f"❌ ValueError: {str(e)}")
            ingresos_salidas_ns.abort(400, error=str(e))
        except Exception as e:
            print(f"❌ ERROR al actualizar ingreso/salida {ingreso_salida_id}: {str(e)}")
            import traceback
            traceback.print_exc()
            ingresos_salidas_ns.abort(500, error=str(e))

    @ingresos_salidas_ns.response(204, 'Ingreso/Salida eliminado exitosamente')
    @ingresos_salidas_ns.response(404, 'Ingreso/Salida no encontrado')
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN])
    def delete(self, ingreso_salida_id):
        """Eliminar un ingreso/salida"""
        try:
            print(f"🔵 DELETE /ingresos-salidas/{ingreso_salida_id}")
            
            input_data = DeleteIngresoSalidaInput(ingreso_salida_id=ingreso_salida_id)
            result = delete_ingreso_salida_use_case.execute(input_data)
            
            if not result.deleted:
                if "no encontrado" in result.message:
                    ingresos_salidas_ns.abort(404, error=result.message)
                else:
                    ingresos_salidas_ns.abort(400, error=result.message)
            
            print(f"✅ Ingreso/Salida {ingreso_salida_id} eliminado exitosamente")
            
            return '', 204
        except ValueError as e:
            print(f"❌ ValueError: {str(e)}")
            ingresos_salidas_ns.abort(400, error=str(e))
        except Exception as e:
            print(f"❌ ERROR al eliminar ingreso/salida {ingreso_salida_id}: {str(e)}")
            import traceback
            traceback.print_exc()
            ingresos_salidas_ns.abort(500, error=str(e))