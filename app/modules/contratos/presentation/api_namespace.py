from flask_restx import Namespace, fields

# Crear namespace
contratos_ns = Namespace('contratos', description='Gestión de contratos')

# Modelo de salida para contrato
contrato_output = contratos_ns.model('ContratoOutput', {
    'id': fields.Integer(description='ID único del contrato'),
    'id_contrato': fields.String(description='ID del contrato'),
    'nombre': fields.String(description='Nombre del contrato'),
    'pk_maquina': fields.Integer(description='ID de la máquina'),
    'pk_cliente': fields.Integer(description='ID del cliente'),
    'pk_obra': fields.Integer(description='ID de la obra'),
    'fecha_inicio': fields.DateTime(description='Fecha de inicio'),
    'estado': fields.String(description='Estado del contrato'),
    'maquina_nombre': fields.String(description='Nombre de la máquina'),
    'cliente_nombre': fields.String(description='Nombre del cliente'),
    'obra_nombre': fields.String(description='Nombre de la obra')
})

# Modelo de respuesta con lista de contratos
contratos_list_response = contratos_ns.model('ContratosListResponse', {
    'success': fields.Boolean(description='Operación exitosa'),
    'data': fields.List(fields.Nested(contrato_output), description='Lista de contratos'),
    'total': fields.Integer(description='Total de contratos'),
    'filtered_by_maquina': fields.Boolean(description='Filtrado por máquina')
})
