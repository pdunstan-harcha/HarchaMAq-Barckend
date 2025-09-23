from flask_restx import Resource
from flask import request
from flask_jwt_extended import jwt_required
from .api_namespace import contratos_ns, contratos_list_response
from ..infrastructure.sqlalchemy_repository import SqlAlchemyContratoRepository
from ..application.list_contratos_by_maquina import ListContratosByMaquinaUseCase
from ..domain.entity import Contrato

# Instanciar repositorio y casos de uso
contratos_repository = SqlAlchemyContratoRepository()
list_contratos_use_case = ListContratosByMaquinaUseCase(repo=contratos_repository)

def _domain_to_dict(contrato: Contrato) -> dict:
    """Convertir entidad de dominio a diccionario para API"""
    return {
        'id': contrato.id,
        'id_contrato': contrato.id_contrato,
        'nombre': contrato.nombre,
        'pk_maquina': contrato.pk_maquina,
        'pk_cliente': contrato.pk_cliente,
        'pk_obra': contrato.pk_obra,
        'fecha_inicio': contrato.fecha_inicio.isoformat() if contrato.fecha_inicio else None,
        'estado': contrato.estado,
        'maquina_nombre': contrato.maquina_nombre,
        'cliente_nombre': contrato.cliente_nombre,
        'obra_nombre': contrato.obra_nombre
    }

@contratos_ns.route('/')
class ContratosList(Resource):
    @jwt_required()
    @contratos_ns.marshal_with(contratos_list_response)
    def get(self):
        """Obtener lista de contratos, opcionalmente filtrados por máquina"""
        try:
            # Obtener parámetro de filtro por máquina
            maquina_id = request.args.get('maquina_id')
            maquina_id_int = int(maquina_id) if maquina_id else None
            
            # Ejecutar caso de uso
            result = list_contratos_use_case.execute(maquina_id=maquina_id_int)
            
            # Convertir entidades de dominio a diccionarios
            contratos_data = [_domain_to_dict(contrato) for contrato in result.data]
            
            return {
                'success': True,
                'data': contratos_data,
                'total': len(contratos_data),
                'filtered_by_maquina': maquina_id is not None
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al obtener contratos: {str(e)}'
            }, 500
