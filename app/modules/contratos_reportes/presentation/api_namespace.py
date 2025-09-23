from flask_restx import Namespace, fields

# Crear namespace para contratos reportes
contratos_reportes_ns = Namespace('contratos_reportes', description='Gestión de Contratos y Reportes')

# Modelos para documentación de la API
contrato_ref_model = contratos_reportes_ns.model('ContratoRef', {
    'id': fields.Integer(required=True, description='ID del contrato'),
    'nombre': fields.String(required=True, description='Nombre del contrato')
})

maquina_ref_model = contratos_reportes_ns.model('MaquinaRef', {
    'id': fields.Integer(required=True, description='ID de la máquina'),
    'nombre': fields.String(required=True, description='Nombre de la máquina')
})

usuario_ref_model = contratos_reportes_ns.model('UsuarioRef', {
    'id': fields.Integer(required=True, description='ID del usuario'),
    'usuario': fields.String(required=True, description='Nombre de usuario')
})

contrato_reporte_model = contratos_reportes_ns.model('ContratoReporte', {
    'pkReporte': fields.Integer(required=True, description='ID del reporte'),
    'ID_REPORTE': fields.String(required=True, description='Código del reporte'),
    'FECHAHORA_INICIO': fields.DateTime(description='Fecha y hora de inicio'),
    'Descripcion': fields.String(description='Descripción del reporte'),
    'MAQUINA_TXT': fields.String(description='Texto de máquina'),
    'CONTRATO_TXT': fields.String(description='Texto del contrato'),
    'USUARIO_TXT': fields.String(description='Texto del usuario'),
    'contrato': fields.Nested(contrato_ref_model, allow_null=True),
    'maquina': fields.Nested(maquina_ref_model, allow_null=True),
    'usuario': fields.Nested(usuario_ref_model, allow_null=True)
})

create_reporte_input = contratos_reportes_ns.model('CreateReporteInput', {
    'ID_REPORTE': fields.String(required=True, description='Código del reporte'),
    'pkContrato': fields.Integer(description='ID del contrato'),
    'pkMaquina': fields.Integer(description='ID de la máquina'),
    'pkUsuario': fields.Integer(description='ID del usuario'),
    'FECHAHORA_INICIO': fields.DateTime(description='Fecha y hora de inicio'),
    'Descripcion': fields.String(description='Descripción del trabajo'),
    'ODOMETRO_INICIAL': fields.Integer(description='Odómetro inicial'),
    'ODOMETRO_FINAL': fields.Integer(description='Odómetro final'),
    'HORAS_TRABAJADAS': fields.Integer(description='Horas trabajadas'),
    'Observaciones': fields.String(description='Observaciones'),
    'MAQUINA_TXT': fields.String(description='Texto de máquina'),
    'CONTRATO_TXT': fields.String(description='Texto del contrato'),
    'USUARIO_TXT': fields.String(description='Texto del usuario')
})

update_reporte_input = contratos_reportes_ns.model('UpdateReporteInput', {
    'Descripcion': fields.String(description='Descripción del trabajo'),
    'ODOMETRO_FINAL': fields.Integer(description='Odómetro final'),
    'HORAS_TRABAJADAS': fields.Integer(description='Horas trabajadas'),
    'Observaciones': fields.String(description='Observaciones'),
    'Estado_Reporte': fields.String(description='Estado del reporte')
})

pagination_model = contratos_reportes_ns.model('Pagination', {
    'page': fields.Integer(required=True, description='Página actual'),
    'total_pages': fields.Integer(required=True, description='Total de páginas'),
    'total_records': fields.Integer(required=True, description='Total de registros')
})

list_response = contratos_reportes_ns.model('ListResponse', {
    'success': fields.Boolean(required=True, description='Estado de la operación'),
    'data': fields.List(fields.Nested(contrato_reporte_model)),
    'page': fields.Integer(description='Página actual'),
    'total_pages': fields.Integer(description='Total de páginas'),
    'total_records': fields.Integer(description='Total de registros')
})

create_response = contratos_reportes_ns.model('CreateResponse', {
    'success': fields.Boolean(required=True, description='Estado de la operación'),
    'pkReporte': fields.Integer(description='ID del reporte creado'),
    'ID_REPORTE': fields.String(description='Código del reporte creado')
})

get_response = contratos_reportes_ns.model('GetResponse', {
    'success': fields.Boolean(required=True, description='Estado de la operación'),
    'data': fields.Nested(contrato_reporte_model, allow_null=True)
})

message_response = contratos_reportes_ns.model('MessageResponse', {
    'success': fields.Boolean(required=True, description='Estado de la operación'),
    'message': fields.String(required=True, description='Mensaje de respuesta')
})
