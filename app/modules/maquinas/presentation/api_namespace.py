from flask_restx import Namespace, fields

# Crear namespace
maquinas_ns = Namespace('maquinas', description='Gestión de maquinaria')

# Modelo de entrada para crear/actualizar máquina
maquina_input = maquinas_ns.model('MaquinaInput', {
    'MAQUINA': fields.String(required=True, description='Nombre de la máquina'),
    'MARCA': fields.String(required=True, description='Marca de la máquina'),
    'MODELO': fields.String(required=True, description='Modelo de la máquina'),
    'PATENTE': fields.String(description='Patente de la máquina'),
    'OBSERVACIONES': fields.String(description='Observaciones adicionales')
})

# Modelo de salida para máquina
maquina_output = maquinas_ns.model('MaquinaOutput', {
    'pkMaquina': fields.Integer(description='ID único de la máquina'),
    'MAQUINA': fields.String(description='Nombre de la máquina'),
    'MARCA': fields.String(description='Marca de la máquina'),
    'MODELO': fields.String(description='Modelo de la máquina'),
    'PATENTE': fields.String(description='Patente de la máquina'),
    'OBSERVACIONES': fields.String(description='Observaciones adicionales'),
    'FECHA_CREACION': fields.DateTime(description='Fecha de creación'),
    'FECHA_ACTUALIZACION': fields.DateTime(description='Fecha de actualización')
})

# Modelo de respuesta con lista de máquinas
maquinas_list_response = maquinas_ns.model('MaquinasListResponse', {
    'success': fields.Boolean(description='Operación exitosa'),
    'data': fields.List(fields.Nested(maquina_output), description='Lista de máquinas'),
    'total': fields.Integer(description='Total de máquinas')
})

# Modelo de respuesta con una máquina
maquina_response = maquinas_ns.model('MaquinaResponse', {
    'success': fields.Boolean(description='Operación exitosa'),
    'data': fields.Nested(maquina_output, description='Información de la máquina'),
    'message': fields.String(description='Mensaje de respuesta')
})