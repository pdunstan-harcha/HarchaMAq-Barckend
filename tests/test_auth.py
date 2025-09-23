# backend/tests/test_auth.py
import pytest
from app.models import User
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='function')
def test_user(db):
    """Create a test user."""
    # Create a test user
    user = User(
        NOMBRE='Patricio',
        APELLIDOS='Dunstan',
        USUARIO='Patricio Dunstan',
        NOMBREUSUARIO='patricio',
        EmailUsuario='patricio@example.com',
        ROL='admin',
        CLAVE=generate_password_hash('Harcha2025*'),
        USUARIO_ID='test_user_1'  # Required field
    )
    db.session.add(user)
    db.session.commit()
    return user

def test_login_user(client, db, test_user):
    """Test user login with test user's credentials."""
    # Test login with correct credentials
    print("Test user created:", test_user.NOMBREUSUARIO, test_user.CLAVE)
    response = client.post('/auth/login', json={
        'username': 'patricio',  # Using NOMBREUSUARIO instead of USUARIO
        'password': 'Harcha2025*'
    })
    print("Login response:", response.get_json())
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert 'user' in data
    assert data['user']['USUARIO'] == 'Patricio Dunstan'

def test_protected_route(client, db, test_user):
    """Test accessing a protected route with test user's credentials."""
    # Login to get token
    login_response = client.post('/auth/login', json={
        'username': 'patricio',  # Using NOMBREUSUARIO instead of USUARIO
        'password': 'Harcha2025*'
    })
    assert login_response.status_code == 200
    token = login_response.get_json()['access_token']

    # Test protected route
    response = client.get(
        '/auth/me',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'USUARIO' in data
    assert data['USUARIO'] == 'Patricio Dunstan'