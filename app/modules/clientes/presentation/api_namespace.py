from flask_restx import Namespace, fields

# Crear namespace
clientes_ns = Namespace('clientes', description='Gestión de clientes')

# Modelo de salida para cliente
cliente_output = clientes_ns.model('ClienteOutput', {
    'id': fields.Integer(description='ID único del cliente'),
    'id_cliente': fields.String(description='ID del cliente'),
    'nombre': fields.String(description='Nombre del cliente'),
    'rut': fields.String(description='RUT del cliente')
})

# Modelo de respuesta con lista de clientes
clientes_list_response = clientes_ns.model('ClientesListResponse', {
    'success': fields.Boolean(description='Operación exitosa'),
    'data': fields.List(fields.Nested(cliente_output), description='Lista de clientes'),
    'total': fields.Integer(description='Total de clientes')
})
