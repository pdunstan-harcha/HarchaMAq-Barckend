from flask_restx import Resource
from flask_jwt_extended import jwt_required
from .api_namespace import obras_ns, obras_list_response
from ..infrastructure.sqlalchemy_repository import SqlAlchemyObraRepository
from ..application.list_obras import ListObrasUseCase
from ..domain.entity import Obra

# Instanciar repositorio y casos de uso
obras_repository = SqlAlchemyObraRepository()
list_obras_use_case = ListObrasUseCase(repo=obras_repository)

def _domain_to_dict(obra: Obra) -> dict:
    """Convertir entidad de dominio a diccionario para API"""
    return {
        'id': obra.id,
        'id_obra': obra.id_obra,
        'nombre': obra.nombre
    }

@obras_ns.route('/')
class ObrasList(Resource):
    @jwt_required()
    @obras_ns.marshal_with(obras_list_response)
    def get(self):
        """Obtener lista de todas las obras"""
        try:
            # Ejecutar caso de uso
            result = list_obras_use_case.execute()
            
            # Convertir entidades de dominio a diccionarios
            obras_data = [_domain_to_dict(obra) for obra in result.data]
            
            return {
                'success': True,
                'data': obras_data,
                'total': len(obras_data)
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al obtener obras: {str(e)}'
            }, 500
