from urllib import response
from flask_restx import Resource
from flask import request, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.security.roles import roles_required, ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_INSPECTOR, ROLE_PETROLERO, ROLE_OPERADOR
from .api_namespace import (
    recargas_ns, 
    recarga_input, 
    recargas_list_response, 
    create_recarga_response,
    recarga_detail_response,
    error_response
)

# Importar la arquitectura DDD
from ..infraestructure.sqlalchemy_repository import SqlAlchemyRecargaRepository
from ..application.listar import ListRecargasUseCase, ListRecargasInput
from ..application.obtener import GetRecargaUseCase, GetRecargaInput
from ..application.crear import CreateRecargaUseCase, CreateRecargaInput
from ..application.actualizar import UpdateRecargaUseCase, UpdateRecargaInput
from ..application.eliminar import DeleteRecargaUseCase, DeleteRecargaInput
from ..domain.entity import Recarga
from .recibo_template import render_recibo_html

# Instanciar repositorio y casos de uso
recargas_repository = SqlAlchemyRecargaRepository()
list_recargas_use_case = ListRecargasUseCase(repo=recargas_repository)
get_recarga_use_case = GetRecargaUseCase(repo=recargas_repository)
create_recarga_use_case = CreateRecargaUseCase(repo=recargas_repository)
update_recarga_use_case = UpdateRecargaUseCase(repo=recargas_repository)
delete_recarga_use_case = DeleteRecargaUseCase(repo=recargas_repository)

def _domain_to_dict(recarga: Recarga) -> dict:
    """Convertir entidad de dominio a diccionario para API - CON estructura anidada"""
    return {
        'id': recarga.id,
        'codigo': recarga.codigo,
        'fecha': recarga.fecha.isoformat() if recarga.fecha else None,
        'litros': recarga.litros,
        'observaciones': recarga.observaciones,
        'odometro': recarga.odometro,
        'kilometros': recarga.kilometros,
        'fechahora_recarga': recarga.fechahora_recarga.isoformat() if recarga.fechahora_recarga else None,
        'patente': recarga.patente,
        'rut_operador': recarga.rut_operador,
        'litros_anterior': recarga.litros_anterior,
        'horometro_anterior': recarga.horometro_anterior,
        'kilometro_anterior': recarga.kilometro_anterior,
        'fecha_anterior': recarga.fecha_anterior.isoformat() if recarga.fecha_anterior else None,
        
        # Referencias como objetos anidados
        'maquina': {
            'id': recarga.maquina.id if recarga.maquina else None,
            'nombre': recarga.maquina.nombre if recarga.maquina else None
        },
        'usuario': {
            'id': recarga.usuario.id if recarga.usuario else None,
            'usuario': recarga.usuario.usuario if recarga.usuario else None
        },
        'operador': {
            'id': recarga.operador.id if recarga.operador else None,
            'usuario': recarga.operador.usuario if recarga.operador else None
        },
        'obra': {
            'id': recarga.obra.id if recarga.obra else None,
            'nombre': recarga.obra.nombre if recarga.obra else None
        },
        'cliente': {
            'id': recarga.cliente.id if recarga.cliente else None,
            'nombre': recarga.cliente.nombre if recarga.cliente else None
        }
    }

@recargas_ns.route('/')
@recargas_ns.doc(description='Operaciones con recargas de combustible')
class RecargasList(Resource):
    
    @recargas_ns.doc(params={
        'page': 'Número de página (default: 1)',
        'per_page': 'Registros por página (10-100, default: 20)',
        'search': 'Búsqueda en código, patente, RUT operador u observaciones'
    })
    @recargas_ns.marshal_with(recargas_list_response)
    @recargas_ns.response(200, 'Lista de recargas obtenida')
    @recargas_ns.response(401, 'Token inválido')
    @recargas_ns.response(403, 'Sin permisos suficientes')
    @recargas_ns.response(500, 'Error interno', error_response)
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_INSPECTOR, ROLE_PETROLERO, ROLE_OPERADOR])
    def get(self):
        """Obtener lista paginada de recargas de combustible"""
        try:
            # Obtener parámetros de query
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            search = request.args.get('search', '', type=str)
            
            # Obtener información del usuario del JWT para filtrado por roles
            user_id = get_jwt_identity()
            jwt_claims = get_jwt()
            user_role = jwt_claims.get('rol', '')
            
            print(f"🔵 RECARGAS - User ID: {user_id}, Role: {user_role}")
            
            # Filtrar por usuario si es PETROLERO u OPERADOR
            user_filter = None
            if 'PETROLERO' in user_role or 'OPERADOR' in user_role:
                user_filter = user_id
                print(f"🔵 RECARGAS - Aplicando filtro de usuario: {user_filter}")
            else:
                print(f"🔵 RECARGAS - Sin filtro de usuario aplicado")
            
            # Crear input para el caso de uso
            input_data = ListRecargasInput(
                page=page,
                per_page=per_page,
                search=search if search else None,
                user_filter=user_filter
            )
            
            # Ejecutar caso de uso
            result = list_recargas_use_case.execute(input_data)
            
            # Convertir datos
            recargas_data = [_domain_to_dict(rec) for rec in result.data]
            
            return {
                'success': True,
                'data': recargas_data,
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
            print(f"❌ ERROR en recargas: {str(e)}")
            import traceback
            traceback.print_exc()
            recargas_ns.abort(500, error=str(e))

    @recargas_ns.expect(recarga_input, validate=True)
    @recargas_ns.marshal_with(create_recarga_response)
    @recargas_ns.response(201, 'Recarga creada exitosamente')
    @recargas_ns.response(400, 'Datos inválidos')
    @recargas_ns.response(401, 'Token inválido')
    @recargas_ns.response(403, 'Sin permisos suficientes')
    @recargas_ns.response(500, 'Error interno', error_response)
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN])
    def post(self):
        """Crear una nueva recarga de combustible"""
        try:
            print("🔵 POST /recargas/ - Iniciando...")
            
            data = request.get_json()
            print(f"🔵 Data recibida: {data}")
            
            # Validación básica
            if not data:
                print("❌ No se recibieron datos")
                recargas_ns.abort(400, error="No se recibieron datos")
            
            # Verificar campos requeridos
            required_fields = ['pkMaquina', 'pkUsuario', 'LITROS']
            for field in required_fields:
                if field not in data or data[field] is None:
                    print(f"❌ Campo requerido faltante: {field}")
                    recargas_ns.abort(400, error=f"Campo requerido: {field}")
            
            print(f"🔵 Creando input para caso de uso...")
            input_data = CreateRecargaInput(payload=data)
            
            print(f"🔵 Ejecutando caso de uso...")
            result = create_recarga_use_case.execute(input_data)
            
            print(f"🔵 Resultado: {result}")
            
            return {
                'success': True,
                'data': {
                    'id': result.id,
                    'codigo': result.codigo
                },
                'message': 'Recarga creada exitosamente'
            }, 201
            
        except ValueError as e:
            print(f"❌ ValueError: {str(e)}")
            recargas_ns.abort(400, error=str(e))
        except Exception as e:
            print(f"❌ ERROR CRÍTICO al crear recarga: {str(e)}")
            import traceback
            traceback.print_exc()
            recargas_ns.abort(500, error=f"Error interno: {str(e)}")

@recargas_ns.route('/<int:recarga_id>')
@recargas_ns.doc(description='Operaciones con recarga específica')
class RecargasDetail(Resource):
    
    @recargas_ns.marshal_with(recarga_detail_response)
    @recargas_ns.response(200, 'Recarga obtenida exitosamente')
    @recargas_ns.response(404, 'Recarga no encontrada')
    @recargas_ns.response(401, 'Token inválido')
    @recargas_ns.response(403, 'Sin permisos suficientes')
    @recargas_ns.response(500, 'Error interno', error_response)
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_INSPECTOR])
    def get(self, recarga_id):
        """Obtener una recarga específica por ID"""
        try:
            print(f"🔵 GET /recargas/{recarga_id}")
            
            input_data = GetRecargaInput(recarga_id=recarga_id)
            result = get_recarga_use_case.execute(input_data)
            
            if not result.found:
                print(f"❌ Recarga {recarga_id} no encontrada")
                recargas_ns.abort(404, error=f"Recarga {recarga_id} no encontrada")
            
            print(f"✅ Recarga {recarga_id} encontrada")
            
            return {
                'success': True,
                'data': _domain_to_dict(result.data)
            }
        except Exception as e:
            print(f"❌ ERROR al obtener recarga {recarga_id}: {str(e)}")
            recargas_ns.abort(500, error=str(e))

    @recargas_ns.expect(recarga_input, validate=False)  # validate=False para permitir campos opcionales
    @recargas_ns.marshal_with(recarga_detail_response)
    @recargas_ns.response(200, 'Recarga actualizada exitosamente')
    @recargas_ns.response(404, 'Recarga no encontrada')
    @recargas_ns.response(400, 'Datos inválidos')
    @recargas_ns.response(401, 'Token inválido')
    @recargas_ns.response(403, 'Sin permisos suficientes')
    @recargas_ns.response(500, 'Error interno', error_response)
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN])
    def put(self, recarga_id):
        """Actualizar completamente una recarga"""
        try:
            print(f"🔵 PUT /recargas/{recarga_id}")
            
            data = request.get_json()
            print(f"🔵 Data recibida: {data}")
            
            if not data:
                recargas_ns.abort(400, error="No se recibieron datos para actualizar")
            
            # Agregar información del usuario que modifica (desde JWT)
            from flask_jwt_extended import get_jwt_identity
            user_id = get_jwt_identity()
            data['pk_usuario_modificacion'] = int(user_id) if user_id else None
            
            input_data = UpdateRecargaInput(recarga_id=recarga_id, payload=data)
            result = update_recarga_use_case.execute(input_data)
            
            if not result.updated:
                if "no encontrada" in result.message:
                    recargas_ns.abort(404, error=result.message)
                else:
                    recargas_ns.abort(400, error=result.message)
            
            print(f"✅ Recarga {recarga_id} actualizada exitosamente")
            
            return {
                'success': True,
                'data': _domain_to_dict(result.data),
                'message': result.message
            }
        except ValueError as e:
            print(f"❌ ValueError en PUT: {str(e)}")
            recargas_ns.abort(400, error=str(e))
        except Exception as e:
            print(f"❌ ERROR al actualizar recarga {recarga_id}: {str(e)}")
            import traceback
            traceback.print_exc()
            recargas_ns.abort(500, error=str(e))

    @recargas_ns.expect(recarga_input, validate=False)  # validate=False para permitir campos opcionales
    @recargas_ns.marshal_with(recarga_detail_response)
    @recargas_ns.response(200, 'Recarga modificada exitosamente')
    @recargas_ns.response(404, 'Recarga no encontrada')
    @recargas_ns.response(400, 'Datos inválidos')
    @recargas_ns.response(401, 'Token inválido')
    @recargas_ns.response(403, 'Sin permisos suficientes')
    @recargas_ns.response(500, 'Error interno', error_response)
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN])
    def patch(self, recarga_id):
        """Modificar parcialmente una recarga (igual que PUT)"""
        try:
            print(f"🔵 PATCH /recargas/{recarga_id}")
            
            data = request.get_json()
            print(f"🔵 Data recibida: {data}")
            
            if not data:
                recargas_ns.abort(400, error="No se recibieron datos para modificar")
            
            # Agregar información del usuario que modifica (desde JWT)
            from flask_jwt_extended import get_jwt_identity
            user_id = get_jwt_identity()
            data['pk_usuario_modificacion'] = int(user_id) if user_id else None
            
            input_data = UpdateRecargaInput(recarga_id=recarga_id, payload=data)
            result = update_recarga_use_case.execute(input_data)
            
            if not result.updated:
                if "no encontrada" in result.message:
                    recargas_ns.abort(404, error=result.message)
                else:
                    recargas_ns.abort(400, error=result.message)
            
            print(f"✅ Recarga {recarga_id} modificada exitosamente")
            
            return {
                'success': True,
                'data': _domain_to_dict(result.data),
                'message': result.message
            }
        except ValueError as e:
            print(f"❌ ValueError en PATCH: {str(e)}")
            recargas_ns.abort(400, error=str(e))
        except Exception as e:
            print(f"❌ ERROR al modificar recarga {recarga_id}: {str(e)}")
            import traceback
            traceback.print_exc()
            recargas_ns.abort(500, error=str(e))

    @recargas_ns.response(204, 'Recarga eliminada exitosamente')
    @recargas_ns.response(404, 'Recarga no encontrada')
    @recargas_ns.response(400, 'No se puede eliminar por dependencias')
    @recargas_ns.response(401, 'Token inválido')
    @recargas_ns.response(403, 'Sin permisos suficientes')
    @recargas_ns.response(500, 'Error interno', error_response)
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN])
    def delete(self, recarga_id):
        """Eliminar una recarga"""
        try:
            print(f"🔵 DELETE /recargas/{recarga_id}")
            
            input_data = DeleteRecargaInput(recarga_id=recarga_id)
            result = delete_recarga_use_case.execute(input_data)
            
            if not result.deleted:
                if "no encontrada" in result.message:
                    recargas_ns.abort(404, error=result.message)
                else:
                    recargas_ns.abort(400, error=result.message)
            
            print(f"✅ Recarga {recarga_id} eliminada exitosamente")
            
            return '', 204  # No content
        except ValueError as e:
            print(f"❌ ValueError en DELETE: {str(e)}")
            recargas_ns.abort(400, error=str(e))
        except Exception as e:
            print(f"❌ ERROR al eliminar recarga {recarga_id}: {str(e)}")
            import traceback
            traceback.print_exc()
            recargas_ns.abort(500, error=str(e))

@recargas_ns.route('/<int:recarga_id>/recibo')
@recargas_ns.doc(description='Generar recibo HTML para impresión térmica de recarga')
class RecargaRecibo(Resource):

    @recargas_ns.response(200, 'Recibo generado exitosamente')
    @recargas_ns.response(404, 'Recarga no encontrada')
    @recargas_ns.response(401, 'Token inválido')
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_INSPECTOR, ROLE_PETROLERO, ROLE_OPERADOR])
    def get(self, recarga_id):

        try:
            input_data = GetRecargaInput(recarga_id=recarga_id)
            result = get_recarga_use_case.execute(input_data)
            if not result.found:
                recargas_ns.abort(404, error=f"Recarga {recarga_id} no encontrada")
            recarga = result.data
            fecha = recarga.fecha.strftime('%d-%m-%Y %H:%M') if recarga.fecha else ''
            html = render_recibo_html(recarga, fecha)
            response = make_response(html)
            response.headers['Content-Type'] = 'text/html'
            return response
        except Exception as e:
            recargas_ns.abort(500, error=str(e))

@recargas_ns.route('/debug/sample')
@recargas_ns.doc(description='Obtener datos de muestra para debug')
class RecargasDebug(Resource):
    
    @recargas_ns.response(200, 'Datos de muestra obtenidos')
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN])
    def get(self):
        """Obtener muestra de campos para debug búsquedas"""
        try:
            from app.models import RecargaCombustible as SARecarga
            
            # Obtener primeros 5 registros con campos importantes
            samples = (
                SARecarga.query
                .with_entities(
                    SARecarga.pkRecarga,
                    SARecarga.ID_RECARGA,
                    SARecarga.PATENTE,
                    SARecarga.RUT_OPERADOR,
                    SARecarga.Observaciones,
                    SARecarga.LITROS,
                    SARecarga.FECHAHORA_RECARGA
                )
                .order_by(SARecarga.FECHAHORA_RECARGA.desc())
                .limit(5)
                .all()
            )
            
            sample_data = []
            for sample in samples:
                sample_data.append({
                    'id': sample.pkRecarga,
                    'codigo': sample.ID_RECARGA,
                    'patente': sample.PATENTE,
                    'rut_operador': sample.RUT_OPERADOR,
                    'observaciones': sample.Observaciones,
                    'litros': sample.LITROS,
                    'fecha': sample.FECHAHORA_RECARGA.isoformat() if sample.FECHAHORA_RECARGA else None
                })
            
            return {
                'success': True,
                'message': 'Muestra de datos para debug',
                'data': sample_data,
                'total_records': SARecarga.query.count()
            }
            
        except Exception as e:
            print(f"❌ ERROR en debug: {str(e)}")
            import traceback
            traceback.print_exc()
            recargas_ns.abort(500, error=str(e))


    