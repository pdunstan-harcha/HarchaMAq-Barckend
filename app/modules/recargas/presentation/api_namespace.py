from flask_restx import Namespace, fields

# Crear namespace para recargas
recargas_ns = Namespace('recargas', description='Gestión de Recargas de Combustible')

# Modelos para documentación de la API
maquina_ref_model = recargas_ns.model('MaquinaRef', {
    'id': fields.Integer(required=True, description='ID de la máquina'),
    'nombre': fields.String(required=True, description='Nombre de la máquina')
})

usuario_ref_model = recargas_ns.model('UsuarioRef', {
    'id': fields.Integer(required=True, description='ID del usuario'),
    'usuario': fields.String(required=True, description='Nombre de usuario')
})

obra_ref_model = recargas_ns.model('ObraRef', {
    'id': fields.Integer(required=True, description='ID de la obra'),
    'nombre': fields.String(required=True, description='Nombre de la obra')
})

cliente_ref_model = recargas_ns.model('ClienteRef', {
    'id': fields.Integer(required=True, description='ID del cliente'),
    'nombre': fields.String(required=True, description='Nombre del cliente')
})

recarga_model = recargas_ns.model('Recarga', {
    'id': fields.Integer(required=True, description='ID de la recarga'),
    'codigo': fields.String(required=True, description='Código de la recarga'),
    'fecha': fields.DateTime(description='Fecha de la recarga'),
    'litros': fields.Integer(description='Litros de combustible'),
    'observaciones': fields.String(description='Observaciones'),
    'odometro': fields.Integer(description='Lectura del odómetro'),
    'kilometros': fields.Integer(description='Kilómetros'),
    'fechahora_recarga': fields.DateTime(description='Fecha y hora de la recarga'),
    'patente': fields.String(description='Patente del vehículo'),
    'rut_operador': fields.String(description='RUT del operador'),
    'litros_anterior': fields.Integer(description='Litros de la recarga anterior'),
    'horometro_anterior': fields.Integer(description='Horómetro anterior'),
    'maquina': fields.Nested(maquina_ref_model, description='Información de la máquina'),
    'usuario': fields.Nested(usuario_ref_model, description='Usuario que registró'),
    'operador': fields.Nested(usuario_ref_model, description='Operador de la máquina'),
    'obra': fields.Nested(obra_ref_model, description='Obra asociada'),
    'cliente': fields.Nested(cliente_ref_model, description='Cliente asociado')
})

pagination_model = recargas_ns.model('Pagination', {
    'total': fields.Integer(required=True, description='Total de registros'),
    'page': fields.Integer(required=True, description='Página actual'),
    'per_page': fields.Integer(required=True, description='Registros por página'),
    'total_pages': fields.Integer(required=True, description='Total de páginas'),
    'has_next': fields.Boolean(required=True, description='Tiene página siguiente'),
    'has_prev': fields.Boolean(required=True, description='Tiene página anterior')
})

recargas_list_response = recargas_ns.model('RecargasListResponse', {
    'success': fields.Boolean(required=True, description='Indica si la operación fue exitosa'),
    'data': fields.List(fields.Nested(recarga_model), description='Lista de recargas'),
    'pagination': fields.Nested(pagination_model, description='Información de paginación')
})

recarga_input = recargas_ns.model('RecargaInput', {
    'pkMaquina': fields.Integer(required=True, description='ID de la máquina'),
    'pkUsuario': fields.Integer(required=True, description='ID del usuario'),
    'LITROS': fields.Integer(required=True, description='Litros de combustible'),
    'OBSERVACIONES': fields.String(description='Observaciones'),
    'ODOMETRO': fields.Integer(description='Lectura del odómetro'),
    'KILOMETROS': fields.Integer(description='Kilómetros'),
    'PATENTE': fields.String(description='Patente del vehículo'),
    'pkOperador': fields.Integer(description='ID del operador'),
    'RUT_OPERADOR': fields.String(description='RUT del operador'),
    'pkObra': fields.Integer(description='ID de la obra'),
    'pkCliente': fields.Integer(description='ID del cliente')
})

create_recarga_response = recargas_ns.model('CreateRecargaResponse', {
    'success': fields.Boolean(required=True, description='Indica si la operación fue exitosa'),
    'data': fields.Raw(description='Datos de la recarga creada'),
    'message': fields.String(required=True, description='Mensaje de confirmación')
})

recarga_detail_response = recargas_ns.model('RecargaDetailResponse', {
    'success': fields.Boolean(required=True, description='Indica si la operación fue exitosa'),
    'data': fields.Nested(recarga_model, description='Datos de la recarga')
})

error_response = recargas_ns.model('ErrorResponse', {
    'error': fields.String(required=True, description='Mensaje de error')
})