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
    
    # Determinar el entorno de ejecución
    flask_env = os.getenv('FLASK_ENV', 'development')
    
    # Cargar variables de entorno según el entorno
    if flask_env == 'production':
        # En producción (Railway), usar variables de entorno del sistema
        # No cargar archivos .env para evitar conflictos
        print("Running in PRODUCTION mode - using system environment variables")
    else:
        # En desarrollo, cargar archivos .env
        env_file = '.env.development' if flask_env == 'development' else '.env'
        env_path = os.path.join(os.path.dirname(__file__), '..', env_file)
        
        if os.path.exists(env_path):
            load_dotenv(env_path, override=True)
            print(f"Loaded environment from {env_file}")
        else:
            load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
            print("Loaded default .env file")
    
    # Configuración de secretos y JWT (deben venir del entorno en producción)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
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
    if flask_env == 'production':
        # En producción, usamos la URL completa que nos pasa Cloud Run
        db_uri = os.getenv('DATABASE_URL')
        # Google Cloud SQL a veces da una URL con 'mysql://'. SQLAlchemy prefiere 'mysql+mysqlconnector://'
        if db_uri and db_uri.startswith("mysql://"):
            db_uri = db_uri.replace("mysql://", "mysql+mysqlconnector://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        print("INFO: Configurando base de datos desde DATABASE_URL para producción.")
    else:
        # Para desarrollo, mantenemos la configuración original desde .env
        db_user = os.getenv('DATABASE_USER')
        db_password = os.getenv('DATABASE_PASSWORD')
        db_host = os.getenv('DATABASE_HOST')
        db_port = os.getenv('DATABASE_PORT')
        db_name = os.getenv('DATABASE_NAME')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        print(f"INFO: Conectando a base de datos de desarrollo.")

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
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