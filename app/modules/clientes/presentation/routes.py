from flask_restx import Resource
from flask_jwt_extended import jwt_required
from .api_namespace import clientes_ns, clientes_list_response
from ..infrastructure.sqlalchemy_repository import SqlAlchemyClienteRepository
from ..application.list_clientes import ListClientesUseCase
from ..domain.entity import Cliente

# Instanciar repositorio y casos de uso
clientes_repository = SqlAlchemyClienteRepository()
list_clientes_use_case = ListClientesUseCase(repo=clientes_repository)

def _domain_to_dict(cliente: Cliente) -> dict:
    """Convertir entidad de dominio a diccionario para API"""
    return {
        'id': cliente.id,
        'id_cliente': cliente.id_cliente,
        'nombre': cliente.nombre,
        'rut': cliente.rut
    }

@clientes_ns.route('/')
class ClientesList(Resource):
    @jwt_required()
    @clientes_ns.marshal_with(clientes_list_response)
    def get(self):
        """Obtener lista de todos los clientes"""
        try:
            # Ejecutar caso de uso
            result = list_clientes_use_case.execute()
            
            # Convertir entidades de dominio a diccionarios
            clientes_data = [_domain_to_dict(cliente) for cliente in result.data]
            
            return {
                'success': True,
                'data': clientes_data,
                'total': len(clientes_data)
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al obtener clientes: {str(e)}'
            }, 500
