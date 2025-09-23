# backend/tests/conftest.py
import os
import pytest
from app import create_app, db as _db
from sqlalchemy.orm import sessionmaker

class TestConfig:
    # Disable loading .env files
    ENV = 'testing'
    
    # Testing flags
    TESTING = True
    DEBUG = True
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    JWT_SECRET_KEY = 'test-secret-key'
    PROPAGATE_EXCEPTIONS = True
    
    # Disable external services
    MAIL_SERVER = None
    REDIS_URL = None
    
    # Override any environment-based configuration
    def __init__(self):
        # Ensure no environment variables affect the test config
        os.environ['SQLALCHEMY_DATABASE_URI'] = self.SQLALCHEMY_DATABASE_URI
        os.environ['DATABASE_USER'] = ''
        os.environ['DATABASE_PASSWORD'] = ''
        os.environ['DATABASE_HOST'] = ''
        os.environ['DATABASE_NAME'] = ''

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for testing."""
    # Create app with test config
    config = TestConfig()
    app = create_app(config)
    
    # Push app context
    app_context = app.app_context()
    app_context.push()
    
    # Initialize database
    with app.app_context():
        _db.create_all()
    
    yield app
    
    # Clean up
    with app.app_context():
        _db.session.remove()
        _db.drop_all()
    
    app_context.pop()

@pytest.fixture(scope='function')
def client(app):
    """A test client for the app."""
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture(scope='function')
def db(app):
    """A test database session."""
    with app.app_context():
        # Drop all tables
        _db.drop_all()
        # Create all tables
        _db.create_all()
        
        # Start a new transaction
        connection = _db.engine.connect()
        transaction = connection.begin()
        
        # Create a session that uses the connection
        testing_session = sessionmaker()(bind=connection)
        
        # Override the session
        _db.session = testing_session
        
        try:
            yield _db
        except Exception as e:
            print(f"Error in test: {str(e)}")
            raise
        finally:
            # Clean up
            testing_session.close()
            transaction.rollback()
            connection.close()
            _db.drop_all()