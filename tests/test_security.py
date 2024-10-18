import pytest
from app import app

def test_password_hashing(app):
    with app.app_context():
        password = 'secure_password123'
        hashed = app.bcrypt.generate_password_hash(password).decode('utf-8')
        assert app.bcrypt.check_password_hash(hashed, password)
        assert not app.bcrypt.check_password_hash(hashed, 'wrong_password')

def test_unauthorized_access(client):
    response = client.get('/admin/meditations')
    assert response.status_code == 302  # Expecting a redirect to login page

