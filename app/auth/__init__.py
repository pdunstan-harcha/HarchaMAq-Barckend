# backend/app/auth/__init__.py
from flask_restx import Namespace, fields

# Crear el namespace
auth_ns = Namespace('auth', description='Autenticación y autorización')

# Definir modelos correctamente DENTRO del namespace
login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='Nombre de usuario'),
    'password': fields.String(required=True, description='Contraseña')
})

user_model = auth_ns.model('User', {
    'pkUsuario': fields.Integer(description='ID del usuario', example=150),
    'USUARIO_ID': fields.String(description='ID de usuario (legacy)', example='pdunstan'),
    'NOMBREUSUARIO': fields.String(description='Nombre de usuario', example='pdunstan'),
    'USUARIO': fields.String(description='Usuario completo', example='Patricio Dunstan'),
    'NOMBRE': fields.String(description='Nombre', example='Patricio'),
    'APELLIDOS': fields.String(description='Apellidos', example='Dunstan'),
    'EMAIL': fields.String(description='Email', example='pdunstan@example.com'),
    'ROL': fields.String(description='Rol del usuario', example='Admin superior'),
    'TELEFONO': fields.String(description='Teléfono', example='+56912345678'),
    'RUT': fields.String(description='RUT', example='12345678-9')
})

# Modelo de respuesta del login
token_response = auth_ns.model('TokenResponse', {
    'success': fields.Boolean(description='Operación exitosa'),
    'access_token': fields.String(description='Token de acceso JWT'),
    'refresh_token': fields.String(description='Token de renovación JWT'),
    'user': fields.Nested(user_model, description='Información del usuario')
})

# Modelo de respuesta del perfil de usuario
user_response = auth_ns.model('UserResponse', {
    'success': fields.Boolean(description='Operación exitosa'),
    'user': fields.Nested(user_model, description='Información del usuario')
})

# Modelo de respuesta de refresh token
refresh_response = auth_ns.model('RefreshResponse', {
    'access_token': fields.String(description='Nuevo token de acceso JWT')
})
# Importar las rutas después de definir los modelos para evitar importaciones circulares
from . import routes  # noqa: E402,F401