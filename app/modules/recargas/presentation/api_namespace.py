from flask_restx import Namespace, fields

# Crear namespace para recargas
recargas_ns = Namespace('recargas', description='Gestión de Recargas de Combustible')

# Modelos para documentación de la API (con campos nullable y ejemplos)
maquina_ref_model = recargas_ns.model('MaquinaRef', {
    'id': fields.Integer(allow_null=True, description='ID de la máquina', example=121),
    'nombre': fields.String(allow_null=True, description='Nombre de la máquina', example='[C-19 RCZX21] - MITSUBISHI L200 4X4 KATANA CRT 2,4CC')
})

usuario_ref_model = recargas_ns.model('UsuarioRef', {
    'id': fields.Integer(allow_null=True, description='ID del usuario', example=150),
    'usuario': fields.String(allow_null=True, description='Nombre de usuario', example='pdunstan'),
    'usuario_id': fields.String(allow_null=True, description='ID de usuario (legacy)', example='pdunstan'),
    'nombre': fields.String(allow_null=True, description='Nombre', example='Patricio'),
    'apellidos': fields.String(allow_null=True, description='Apellidos', example='Dunstan'),
    'rol': fields.String(allow_null=True, description='Rol del usuario', example='Admin superior'),
    'email': fields.String(allow_null=True, description='Email', example='pdunstan@example.com'),
    'telefono': fields.String(allow_null=True, description='Teléfono', example='+56912345678'),
    'rut': fields.String(allow_null=True, description='RUT', example='12345678-9')
})

obra_ref_model = recargas_ns.model('ObraRef', {
    'id': fields.Integer(allow_null=True, description='ID de la obra', example=38),
    'nombre': fields.String(allow_null=True, description='Nombre de la obra', example='CLIENTES')
})

cliente_ref_model = recargas_ns.model('ClienteRef', {
    'id': fields.Integer(allow_null=True, description='ID del cliente', example=9),
    'nombre': fields.String(allow_null=True, description='Nombre del cliente', example='HARCHA')
})

recarga_model = recargas_ns.model('Recarga', {
    'id': fields.Integer(required=True, description='ID de la recarga', example=3241),
    'codigo': fields.String(required=True, description='Código de la recarga', example='RCO00003241'),
    'fecha': fields.DateTime(allow_null=True, description='Fecha de la recarga', example='2025-10-01T00:00:00'),
    'litros': fields.Integer(allow_null=True, description='Litros de combustible', example=58),
    'foto': fields.String(allow_null=True, description='URL de la foto de la recarga', example=None),
    'observaciones': fields.String(allow_null=True, description='Observaciones', example='Recarga completa'),
    'odometro': fields.Integer(allow_null=True, description='Lectura del odómetro', example=25010),
    'kilometros': fields.Integer(allow_null=True, description='Kilómetros', example=167883),
    'fechahora_recarga': fields.DateTime(allow_null=True, description='Fecha y hora de la recarga', example='2025-10-01T09:23:01'),
    'patente': fields.String(allow_null=True, description='Patente del vehículo', example='RCZX21'),
    'rut_operador': fields.String(allow_null=True, description='RUT del operador', example='12345678-9'),
    'id_recarga_anterior': fields.String(allow_null=True, description='ID de la recarga anterior', example='RCO00002972'),
    'litros_anterior': fields.Integer(allow_null=True, description='Litros de la recarga anterior', example=67),
    'horometro_anterior': fields.Integer(allow_null=True, description='Horómetro anterior', example=25000),
    'kilometro_anterior': fields.Integer(allow_null=True, description='Kilómetro anterior', example=167882),
    'fecha_anterior': fields.DateTime(allow_null=True, description='Fecha de la recarga anterior', example='2025-06-25T17:03:39'),
    'maquina': fields.Nested(maquina_ref_model, allow_null=True, description='Información de la máquina'),
    'usuario': fields.Nested(usuario_ref_model, allow_null=True, description='Usuario que registró'),
    'operador': fields.Nested(usuario_ref_model, allow_null=True, description='Operador de la máquina'),
    'obra': fields.Nested(obra_ref_model, allow_null=True, description='Obra asociada'),
    'cliente': fields.Nested(cliente_ref_model, allow_null=True, description='Cliente asociado'),
    'usuario_ultima_modificacion': fields.Nested(usuario_ref_model, allow_null=True, description='Usuario que modificó por última vez')
})

pagination_model = recargas_ns.model('Pagination', {
    'total': fields.Integer(required=True, description='Total de registros', example=3241),
    'page': fields.Integer(required=True, description='Página actual', example=1),
    'per_page': fields.Integer(required=True, description='Registros por página', example=20),
    'total_pages': fields.Integer(required=True, description='Total de páginas', example=163),
    'has_next': fields.Boolean(required=True, description='Tiene página siguiente', example=True),
    'has_prev': fields.Boolean(required=True, description='Tiene página anterior', example=False)
})

recargas_list_response = recargas_ns.model('RecargasListResponse', {
    'success': fields.Boolean(required=True, description='Indica si la operación fue exitosa'),
    'data': fields.List(fields.Nested(recarga_model), description='Lista de recargas'),
    'pagination': fields.Nested(pagination_model, description='Información de paginación')
})

recarga_input = recargas_ns.model('RecargaInput', {
    'pkMaquina': fields.Integer(required=True, description='ID de la máquina', example=121),
    'pkUsuario': fields.Integer(required=True, description='ID del usuario', example=150),
    'LITROS': fields.Integer(required=True, description='Litros de combustible', example=58),
    'OBSERVACIONES': fields.String(description='Observaciones', example='Recarga completa'),
    'ODOMETRO': fields.Integer(description='Lectura del odómetro', example=25010),
    'KILOMETROS': fields.Integer(description='Kilómetros', example=167883),
    'PATENTE': fields.String(description='Patente del vehículo', example='RCZX21'),
    'pkOperador': fields.Integer(description='ID del operador', example=145),
    'RUT_OPERADOR': fields.String(description='RUT del operador', example='12345678-9'),
    'pkObra': fields.Integer(description='ID de la obra', example=38),
    'pkCliente': fields.Integer(description='ID del cliente', example=9),

    # Campos de recarga anterior (opcionales, enviados automáticamente por el frontend)
    'pkRecarga_anterior': fields.Integer(description='ID de la recarga anterior', example=2972),
    'ID_Recarga_Anterior': fields.String(description='Código de la recarga anterior', example='RCO00002972'),
    'Litros_Anterior': fields.Integer(description='Litros de la recarga anterior', example=67),
    'Horometro_Anterior': fields.Integer(description='Horómetro de la recarga anterior', example=25000),
    'Kilometro_Anterior': fields.Integer(description='Kilómetros de la recarga anterior', example=167882),
    'Fecha_Anterior': fields.DateTime(description='Fecha de la recarga anterior', example='2025-06-25T17:03:39')
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