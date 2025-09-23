from functools import wraps
from typing import Iterable, Callable, Any, Optional
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

# Role constants 
ROLE_ADMIN = "ADMIN"
ROLE_SUPER_ADMIN = "SUPER ADMIN"
ROLE_INSPECTOR = "INSPECTOR"
ROLE_PETROLERO = "PETROLERO"
ROLE_OPERADOR = "OPERADOR"
ROLE_OPERADOR = "OPERADOR"

def normalize_role(role: str) -> str:
    """Normalize role for comparison - MAPEO ESPECÍFICO PARA TU BD"""
    if not role:
        return ""
    
    # ✅ Mapear exactamente los roles de tu base de datos
    role_clean = role.strip().upper()
    
    if "ADMIN SUPERIOR" in role_clean:
        return ROLE_SUPER_ADMIN
    elif role_clean == "ADMIN":
        return ROLE_ADMIN
    elif "INSPECTOR" in role_clean:
        return ROLE_INSPECTOR
    elif "PETROLERO" in role_clean:
        return ROLE_PETROLERO
    elif "OPERADOR" in role_clean:
        return ROLE_OPERADOR
    
    # Si no encuentra mapeo, devolver como está (uppercase)
    return role_clean

def roles_required(required_roles: Iterable[str]) -> Callable[[Callable], Callable]:
    """
    Decorator to require specific roles for accessing an endpoint.
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs) -> Any:
            # Obtener claims del JWT
            jwt_data = get_jwt()
            user_role = jwt_data.get("rol", "")
            
            # Debug detallado
            print(f"\n🔍 === DEBUG ROLES ===")
            print(f"🔍 JWT Data: {jwt_data}")
            print(f"🔍 Usuario rol (raw): '{user_role}'")
            
            if not user_role:
                print("❌ No se encontró rol en el token")
                return jsonify({"message": "No se encontró rol en el token"}), 403
            
            # Normalize both user role and required roles
            normalized_user_role = normalize_role(user_role)
            normalized_required_roles = [normalize_role(role) for role in required_roles]
            
            print(f"🔍 Usuario rol (normalizado): '{normalized_user_role}'")
            print(f"🔍 Roles requeridos: {required_roles}")
            print(f"🔍 Roles requeridos (normalizados): {normalized_required_roles}")
            print(f"🔍 ¿Acceso permitido?: {normalized_user_role in normalized_required_roles}")
            print(f"🔍 === FIN DEBUG ===\n")
            
            if normalized_user_role not in normalized_required_roles:
                return jsonify({
                    "message": f"Acceso denegado. Roles requeridos: {required_roles}, tu rol: '{user_role}' -> '{normalized_user_role}'"
                }), 403
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator