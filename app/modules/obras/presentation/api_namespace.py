from flask_restx import Namespace, fields

# Crear namespace
obras_ns = Namespace('obras', description='Gestión de obras')

# Modelo de salida para obra
obra_output = obras_ns.model('ObraOutput', {
    'id': fields.Integer(description='ID único de la obra'),
    'id_obra': fields.String(description='ID de la obra'),
    'nombre': fields.String(description='Nombre de la obra')
})

# Modelo de respuesta con lista de obras
obras_list_response = obras_ns.model('ObrasListResponse', {
    'success': fields.Boolean(description='Operación exitosa'),
    'data': fields.List(fields.Nested(obra_output), description='Lista de obras'),
    'total': fields.Integer(description='Total de obras')
})
