from flask_restx import Resource
from flask import request
from flask_jwt_extended import jwt_required
from app.security.roles import (
    ROLE_OPERADOR,
    ROLE_PETROLERO,
    ROLE_PORTERO,
    ROLE_ADMIN,
    ROLE_SUPER_ADMIN,
    ROLE_INSPECTOR,
    roles_required,
)
from .api_namespace import (
    maquinas_ns, 
    maquina_input, 
    maquina_output, 
    maquinas_list_response, 
    maquina_response
)

# Importar la arquitectura DDD
from ..infrastructure.sqlalchemy_repository import SqlAlchemyMaquinaRepository
from ..application.List_maquinas import ListMaquinasUseCase
from ..domain.entity import Maquina as MaquinaDomain
from ..application.get_operadores_by_maquina_id import GetOperadoresByMaquinaIdUseCase

# Instanciar repositorio y casos de uso
maquinas_repository = SqlAlchemyMaquinaRepository()
list_maquinas_use_case = ListMaquinasUseCase(repo=maquinas_repository)
get_operadores_uc = GetOperadoresByMaquinaIdUseCase(repo=maquinas_repository)

def _domain_to_dict(maquina: MaquinaDomain) -> dict:
    """Convertir entidad de dominio a diccionario para API"""
    return {
        'pkMaquina': maquina.id,
        'MAQUINA': maquina.nombre,
        'MARCA': maquina.marca,
        'MODELO': maquina.modelo,
        'PATENTE': maquina.patente,
        'ESTADO': maquina.estado,
        'ID_MAQUINA': maquina.id_maquina,

        # ✅ NUEVO - Datos de última recarga
        'HR_Actual': maquina.hr_actual,
        'KM_Actual': maquina.km_actual,
        'pkUltima_recarga': maquina.pk_ultima_recarga,
        'ID_Ultima_Recarga': maquina.id_ultima_recarga,
        'Litros_Ultima': maquina.litros_ultima,
        'Fecha_Ultima': maquina.fecha_ultima.isoformat() if maquina.fecha_ultima else None,

        'OPERADORES': [
            {
                'id': op.id,
                'usuario': op.usuario,
                'nombre': op.nombre,
                'usuario_id': op.usuario_id,
                'nombre_completo': op.usuario_id  # Este es el nombre completo según tu BD
            } for op in maquina.operadores
        ] if maquina.operadores else []
    }

def _operador_to_dict(operador) -> dict:
    """Convertir OperadorRef a diccionario para API"""
    return {
        'id': operador.id,
        'nombre': operador.nombre,
        'usuario': operador.usuario,
        'usuario_id': operador.usuario_id,
        'nombre_completo': operador.usuario_id  # USUARIO_ID contiene el nombre completo
    }

@maquinas_ns.route('/')
@maquinas_ns.doc(description='Operaciones con máquinas')
class MaquinasList(Resource):
    @maquinas_ns.marshal_with(maquinas_list_response)
    @maquinas_ns.response(200, 'Lista de máquinas obtenida')
    @maquinas_ns.response(401, 'Token inválido')
    @maquinas_ns.response(403, 'Sin permisos suficientes')
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_INSPECTOR, ROLE_OPERADOR, ROLE_PETROLERO, ROLE_PORTERO])
    def get(self):
        """Obtener lista de todas las máquinas usando arquitectura DDD"""
        try:
            # Usar el caso de uso de DDD
            result = list_maquinas_use_case.execute()
            maquinas_domain = result.data  # ListMaquinasOutput.data
            
            # Convertir entidades de dominio a formato API
            maquinas_data = [_domain_to_dict(maq) for maq in maquinas_domain]
            
            return {
                'success': True,
                'data': maquinas_data,
                'total': len(maquinas_data)
            }
        except Exception as e:
            maquinas_ns.abort(500, f"Error al obtener máquinas: {str(e)}")

@maquinas_ns.route('/<int:maquina_id>')
@maquinas_ns.doc(description='Operaciones con una máquina específica')
class MaquinaDetail(Resource):
    @maquinas_ns.marshal_with(maquina_response)
    @maquinas_ns.response(200, 'Máquina obtenida')
    @maquinas_ns.response(404, 'Máquina no encontrada')
    @maquinas_ns.response(401, 'Token inválido')
    @maquinas_ns.response(403, 'Sin permisos suficientes')
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_INSPECTOR, ROLE_OPERADOR, ROLE_PETROLERO, ROLE_PORTERO])
    def get(self, maquina_id):
        """Obtener una máquina específica por ID con datos de última recarga"""
        try:
            # ✅ Usar get_by_id directamente para obtener datos completos incluyendo última recarga
            maquina = maquinas_repository.get_by_id(maquina_id)

            if not maquina:
                maquinas_ns.abort(404, f"Máquina con ID {maquina_id} no encontrada")

            return {
                'success': True,
                'data': _domain_to_dict(maquina),
                'message': 'Máquina obtenida exitosamente'
            }

        except Exception as e:
            maquinas_ns.abort(500, f"Error al obtener máquina: {str(e)}")

@maquinas_ns.route('/<int:maquina_id>/operadores')
@maquinas_ns.doc(description='Obtener operadores asignados a una máquina específica')
class MaquinaOperadores(Resource):
    @maquinas_ns.response(200, 'Operadores de la máquina obtenidos')
    @maquinas_ns.response(404, 'Máquina no encontrada')
    @maquinas_ns.response(401, 'Token inválido')
    @maquinas_ns.response(403, 'Sin permisos suficientes')
    @jwt_required()
    @roles_required([ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_INSPECTOR, ROLE_OPERADOR, ROLE_PETROLERO, ROLE_PORTERO])
    def get(self, maquina_id):
        """Obtener operadores asignados a una máquina específica"""
        try:
            print(f"ENDPOINT - Solicitando operadores para máquina ID: {maquina_id}")
            
            operadores = get_operadores_uc.execute(maquina_id)
            
            print(f"ENDPOINT - UseCase retornó {len(operadores)} operadores")
            
            # Mapear operadores con debug detallado
            operadores_data = []
            for i, op in enumerate(operadores):
                print(f"ENDPOINT - Procesando operador {i+1}:")
                print(f"  - Raw OperadorRef: {op}")
                
                operador_dict = _operador_to_dict(op)
                operadores_data.append(operador_dict)
                
                print(f"  - Mapeado a dict: {operador_dict}")
            
            response_data = {
                'success': True,
                'data': operadores_data,
                'total': len(operadores_data),
                'maquina_id': maquina_id
            }
            
            print(f"ENDPOINT - Response final: {response_data}")
            return response_data
            
        except Exception as e:
            print(f"ERROR en endpoint operadores: {str(e)}")
            import traceback
            traceback.print_exc()
            maquinas_ns.abort(500, f"Error al obtener operadores de la máquina: {str(e)}")