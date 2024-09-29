import pytest

def test_password_hashing(app):
    with app.app_context():
        password = 'secure_password123'
        hashed = app.bcrypt.generate_password_hash(password).decode('utf-8')
        assert app.bcrypt.check_password_hash(hashed, password)
        assert not app.bcrypt.check_password_hash(hashed, 'wrong_password')

def test_unauthorized_access(client):
    response = client.get('/admin/meditations')
    assert response.status_code == 302  # Expecting a redirect to login page

def test_csrf_protection(client):
    response = client.post('/login', data={'username': 'test', 'password': 'test'})
    assert response.status_code == 200
    assert b'csrf_token' in response.data

# Add more security tests (e.g., XSS protection, SQL injection prevention)