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
    'pkUsuario': fields.Integer(description='ID del usuario'),
    'NOMBREUSUARIO': fields.String(description='Nombre de usuario'),
    'NOMBRE': fields.String(description='Nombre'),
    'APELLIDOS': fields.String(description='Apellidos'),
    'EMAIL': fields.String(description='Email'),
    'ROL': fields.String(description='Rol del usuario')
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