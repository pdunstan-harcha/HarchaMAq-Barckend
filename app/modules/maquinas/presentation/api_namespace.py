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
    'ESTADO': fields.String(description='Estado de la máquina'),
    'ID_MAQUINA': fields.String(description='ID de la máquina'),
    'OBSERVACIONES': fields.String(description='Observaciones adicionales'),
    'FECHA_CREACION': fields.DateTime(description='Fecha de creación'),
    'FECHA_ACTUALIZACION': fields.DateTime(description='Fecha de actualización'),

    # ✅ NUEVO - Datos de última recarga
    'HR_Actual': fields.Integer(allow_null=True, description='Horómetro actual', example=15234),
    'KM_Actual': fields.Integer(allow_null=True, description='Kilómetros actuales', example=45678),
    'pkUltima_recarga': fields.Integer(allow_null=True, description='ID de la última recarga', example=3244),
    'ID_Ultima_Recarga': fields.String(allow_null=True, description='Código de la última recarga', example='RCO00003244'),
    'Litros_Ultima': fields.Integer(allow_null=True, description='Litros de la última recarga', example=42),
    'Fecha_Ultima': fields.String(allow_null=True, description='Fecha de la última recarga', example='2025-10-02T00:56:12'),

    'OPERADORES': fields.Raw(description='Lista de operadores asignados')
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