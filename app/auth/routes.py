from flask_restx import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from datetime import timedelta
from . import auth_ns, login_model, token_response, user_response, refresh_response
from ..models import User

@auth_ns.route('/login')
@auth_ns.doc(description='Iniciar sesión y obtener token JWT')
class Login(Resource):
    @auth_ns.expect(login_model, validate=True)
    @auth_ns.marshal_with(token_response)
    @auth_ns.response(200, 'Login exitoso')
    @auth_ns.response(400, 'Credenciales faltantes')
    @auth_ns.response(401, 'Credenciales inválidas')
    def post(self):
        """Iniciar sesión y obtener tokens JWT"""
        data = request.get_json()
        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username or not password:
            auth_ns.abort(400, "Username y password son requeridos")

        user = User.query.filter_by(NOMBREUSUARIO=username).first()
        
        if not user:
            auth_ns.abort(401, "Usuario o contraseña incorrectos")

        # Verificar contraseña (ajusta según tu lógica)
        if user.CLAVE != password:  # Simplificado - usa hash en producción
            auth_ns.abort(401, "Usuario o contraseña incorrectos")

        # ✅ IDENTITY DEBE SER STRING + ADDITIONAL CLAIMS
        identity = str(user.pkUsuario)  # Solo string para subject
        
        additional_claims = {
            "username": user.NOMBREUSUARIO,
            "rol": user.ROL,
            "nombre": user.NOMBRE,
            "apellidos": user.APELLIDOS
        }
        
        access_token = create_access_token(
            identity=identity, 
            additional_claims=additional_claims,
            expires_delta=timedelta(hours=6)
        )
        refresh_token = create_refresh_token(
            identity=identity,
            additional_claims=additional_claims
        )

        return {
            "success": True,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "pkUsuario": user.pkUsuario,
                "NOMBREUSUARIO": user.NOMBREUSUARIO,
                "NOMBRE": user.NOMBRE,
                "APELLIDOS": user.APELLIDOS,
                "EMAIL": getattr(user, 'EmailUsuario', ''),
                "ROL": user.ROL
            }
        }

@auth_ns.route('/me')
@auth_ns.doc(description='Obtener información del usuario autenticado')
class UserProfile(Resource):
    @auth_ns.marshal_with(user_response)
    @auth_ns.response(200, 'Información del usuario')
    @auth_ns.response(401, 'Token inválido')
    @auth_ns.response(404, 'Usuario no encontrado')
    @jwt_required()
    def get(self):
        """Obtener perfil del usuario autenticado"""
        current_user_identity = get_jwt_identity()  # String: user_id
        user_id = int(current_user_identity)
            
        user = User.query.get(user_id)
        
        if not user:
            auth_ns.abort(404, "Usuario no encontrado")
            
        return {
            "success": True,
            "user": {
                "pkUsuario": user.pkUsuario,
                "NOMBREUSUARIO": user.NOMBREUSUARIO,
                "NOMBRE": user.NOMBRE,
                "APELLIDOS": user.APELLIDOS,
                "EMAIL": getattr(user, 'EmailUsuario', ''),
                "ROL": user.ROL
            }
        }

@auth_ns.route('/refresh')
@auth_ns.doc(description='Renovar token de acceso')
class RefreshToken(Resource):
    @auth_ns.marshal_with(refresh_response)
    @auth_ns.response(200, 'Token renovado')
    @auth_ns.response(401, 'Refresh token inválido')
    @jwt_required(refresh=True)
    def post(self):
        """Renovar access token usando refresh token"""
        current_user_identity = get_jwt_identity()
        new_token = create_access_token(identity=current_user_identity, expires_delta=timedelta(hours=6))
        return {"access_token": new_token}