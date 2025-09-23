from flask_restx import Namespace, fields

# Crear namespace para ingresos/salidas
ingresos_salidas_ns = Namespace('ingresos_salidas', description='Gestión de Ingresos y Salidas de Máquinas')

# ✅ MODELO PARA MÁQUINAS DISPONIBLES (FALTABA)
maquina_simple_model = ingresos_salidas_ns.model('MaquinaSimple', {
    'id': fields.Integer(required=True, description='ID de la máquina'),
    'nombre': fields.String(required=True, description='Nombre completo con código'),
    'codigo': fields.String(description='Código de la máquina (ej: MB-01)'),
    'ultimo_movimiento': fields.String(description='Descripción del último movimiento'),
    'puede_ingresar': fields.Boolean(description='Si puede registrar INGRESO'),
    'puede_salir': fields.Boolean(description='Si puede registrar SALIDA')
})

# ✅ RESPUESTA DE MÁQUINAS DISPONIBLES (FALTABA)
maquinas_disponibles_response = ingresos_salidas_ns.model('MaquinasDisponiblesResponse', {
    'success': fields.Boolean(required=True, description='Estado de la operación'),
    'data': fields.List(
        fields.Nested(maquina_simple_model), 
        description='Lista de máquinas con estado de movimientos'
    )
})

# Modelos para referencias
maquina_ref_model = ingresos_salidas_ns.model('MaquinaRef', {
    'id': fields.Integer(required=True, description='ID de la máquina'),
    'nombre': fields.String(required=True, description='Nombre de la máquina'),
    'codigo': fields.String(description='Código de la máquina')
})

usuario_ref_model = ingresos_salidas_ns.model('UsuarioRef', {
    'id': fields.Integer(required=True, description='ID del usuario'),
    'usuario': fields.String(required=True, description='Nombre de usuario'),
    'nombre_completo': fields.String(description='Nombre completo del usuario')
})

# ✅ MODELO DE ENTRADA mejorado
ingreso_salida_input = ingresos_salidas_ns.model('IngresoSalidaInput', {
    'pkMaquina': fields.Integer(required=True, description='ID de la máquina'),
    'pkUsuario': fields.Integer(required=True, description='ID del usuario'),
    'INGRESO_SALIDA': fields.String(
        required=True, 
        description='Tipo de movimiento', 
        enum=['INGRESO', 'SALIDA']
    ),
    'FECHAHORA': fields.DateTime(
        description='Fecha y hora del movimiento (formato: YYYY-MM-DD HH:MM:SS)'
    ),
    'ESTADO_MAQUINA': fields.String(
        description='Estado de la máquina',
        enum=['OPERATIVA', 'MANTENIMIENTO', 'REPARACION', 'FUERA_DE_SERVICIO', 'EN_PRODUCCION']
    ),
    'Observaciones': fields.String(description='Observaciones del movimiento'),
    'editar_fecha': fields.String(
        description='¿Permitir editar fecha? (SI/NO)', 
        enum=['SI', 'NO'], 
        default='NO'
    ),
    'Control1': fields.Integer(description='Campo de control adicional')
})

# ✅ MODELO DE RESPUESTA mejorado
ingreso_salida_model = ingresos_salidas_ns.model('IngresoSalida', {
    'id': fields.Integer(required=True, description='ID del registro'),
    'codigo': fields.String(description='Código del ingreso/salida'),
    'fechahora': fields.DateTime(description='Fecha y hora del movimiento'),
    'ingreso_salida': fields.String(description='Tipo: INGRESO o SALIDA'),
    'estado_maquina': fields.String(description='Estado de la máquina'),
    'tiempo': fields.String(description='Tiempo calculado (HH:MM:SS)'),
    'tiempo_formateado': fields.String(description='Tiempo en formato legible'),
    'observaciones': fields.String(description='Observaciones'),
    'editar_fecha': fields.String(description='Si fue editado (SI/NO)'),
    'fecha_editada': fields.DateTime(description='Fecha de edición'),
    
    # Campos del movimiento anterior
    'movimiento_anterior_texto': fields.String(description='Descripción del movimiento anterior'),
    'fechahora_ultimo': fields.DateTime(description='Fecha del último movimiento'),
    'puede_modificar_fecha': fields.Boolean(description='Si puede modificar la fecha'),
    
    # Referencias
    'maquina_id': fields.Integer(description='ID de la máquina'),
    'maquina_nombre': fields.String(description='Nombre de la máquina'),
    'maquina_codigo': fields.String(description='Código de la máquina (ej: MB-01)'),
    'usuario_id': fields.Integer(description='ID del usuario'),
    'usuario_nombre': fields.String(description='Nombre del usuario')
})

# Modelos de paginación
pagination_model = ingresos_salidas_ns.model('Pagination', {
    'total': fields.Integer(required=True, description='Total de registros'),
    'page': fields.Integer(required=True, description='Página actual'),
    'per_page': fields.Integer(required=True, description='Registros por página'),
    'total_pages': fields.Integer(required=True, description='Total de páginas'),
    'has_next': fields.Boolean(required=True, description='Tiene página siguiente'),
    'has_prev': fields.Boolean(required=True, description='Tiene página anterior')
})

# Modelos de respuesta
ingresos_salidas_list_response = ingresos_salidas_ns.model('IngresosSalidasListResponse', {
    'success': fields.Boolean(required=True, description='Indica si la operación fue exitosa'),
    'data': fields.List(fields.Nested(ingreso_salida_model), description='Lista de ingresos/salidas'),
    'pagination': fields.Nested(pagination_model, description='Información de paginación')
})

create_ingreso_salida_response = ingresos_salidas_ns.model('CreateIngresoSalidaResponse', {
    'success': fields.Boolean(required=True, description='Indica si la operación fue exitosa'),
    'data': fields.Nested(ingreso_salida_model, description='Datos del ingreso/salida creado'),
    'message': fields.String(required=True, description='Mensaje de confirmación')
})

ingreso_salida_detail_response = ingresos_salidas_ns.model('IngresoSalidaDetailResponse', {
    'success': fields.Boolean(required=True, description='Indica si la operación fue exitosa'),
    'data': fields.Nested(ingreso_salida_model, description='Datos del ingreso/salida')
})

error_response = ingresos_salidas_ns.model('ErrorResponse', {
    'error': fields.String(required=True, description='Mensaje de error')
})