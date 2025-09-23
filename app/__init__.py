import os
import datetime
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restx import Api, Resource

# Instancia global de SQLAlchemy
db = SQLAlchemy()

def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    
    # Cargar variables de entorno desde .env.development
    env_file = '.env.development'
    env_path = os.path.join(os.path.dirname(__file__), '..', env_file)
    
    if os.path.exists(env_path):
        load_dotenv(env_path, override=True)
        print(f"Loaded environment from {env_file}")
    else:
        load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
        print("Loaded default .env file")
    
    # Debug: Mostrar variables de entorno cargadas
    print("\n=== Variables de entorno cargadas ===")
    for var in ['DATABASE_USER', 'DATABASE_HOST', 'DATABASE_PORT', 'DATABASE_NAME', 'FLASK_ENV']:
        print(f"{var}: {os.getenv(var, 'No definida')}")
    print("=================================\n")
    
    # Configuración básica
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # ✅ Configuración JWT COMPLETA
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "your-secret-string")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=6)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=30)
    jwt = JWTManager(app)
    
    # CORS
    allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*")
    if allowed_origins and allowed_origins != "*":
        origins = [o.strip() for o in allowed_origins.split(",") if o.strip()]
        CORS(app, resources={r"/*": {"origins": origins}})
    else:
        CORS(app)

    # Configuración de base de datos
    db_user = os.getenv('DATABASE_USER')
    db_password = os.getenv('DATABASE_PASSWORD')
    db_host = os.getenv('DATABASE_HOST')
    db_port = os.getenv('DATABASE_PORT')
    db_name = os.getenv('DATABASE_NAME')
    
    db_uri_debug = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri_debug
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    print(f"Conectando a MySQL en: mysql+mysqlconnector://{db_user}:*****@{db_host}:{db_port}/{db_name}")
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Importar modelos
    from . import models
    
    # Crear tablas
    with app.app_context():
        db.create_all()
        print("Base de datos inicializada correctamente")
    
    # Configuración de Flask-RESTX
    authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Ingresa: Bearer {token}'
        }
    }

    # Crear API
    api = Api(
        app,
        version='1.0',
        title='HarchaMAq API',
        description='Sistema de gestión de maquinaria',
        doc='/docs/',
        authorizations=authorizations,
        security='Bearer'
    )

    # Importar y registrar namespaces
    from .auth import auth_ns
    api.add_namespace(auth_ns, path='/auth')

    # Máquinas
    from .modules.maquinas.presentation.api_namespace import maquinas_ns
    from .modules.maquinas.presentation import routes
    api.add_namespace(maquinas_ns, path='/maquinas')

     
    # RECARGAS
    from .modules.recargas.presentation.api_namespace import recargas_ns
    from .modules.recargas.presentation import routes as recargas_routes
    api.add_namespace(recargas_ns, path='/recargas')


    #INGRESOS Y SALIDAS - Módulo completo DDD
    from .modules.ingresos_salidas.presentation.schemas import ingresos_salidas_ns
    from .modules.ingresos_salidas.presentation import routes as ingresos_salidas_routes
    api.add_namespace(ingresos_salidas_ns, path='/ingresos_salidas')
    
    # CONTRATOS REPORTES - Módulo completo DDD  
    from .modules.contratos_reportes.presentation.api_namespace import contratos_reportes_ns
    from .modules.contratos_reportes.presentation import routes as contratos_reportes_routes
    api.add_namespace(contratos_reportes_ns, path='/contratos_reportes')
    
        # CLIENTES - Módulo DDD completo
    from .modules.clientes.presentation.api_namespace import clientes_ns
    from .modules.clientes.presentation import routes as clientes_routes
    api.add_namespace(clientes_ns, path='/clientes')
    
    # OBRAS - Módulo DDD completo  
    from .modules.obras.presentation.api_namespace import obras_ns
    from .modules.obras.presentation import routes as obras_routes
    api.add_namespace(obras_ns, path='/obras')
    
    # CONTRATOS - Módulo DDD completo
    from .modules.contratos.presentation.api_namespace import contratos_ns
    from .modules.contratos.presentation import routes as contratos_routes
    api.add_namespace(contratos_ns, path='/contratos')
    
    # Health check
    @api.route('/health')
    class HealthCheck(Resource):
        def get(self):
            """Verificar estado de la API"""
            return {
                'status': 'ok',
                'message': 'API funcionando',
                'timestamp': datetime.datetime.utcnow().isoformat()
            }
    
    return app