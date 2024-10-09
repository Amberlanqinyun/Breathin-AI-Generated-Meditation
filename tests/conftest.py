import sys
import os
import pytest

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mod_utilize import app as flask_app  # Import the app instance from mod_utilize
from mod_db_account import search_user, create_user, hash_password
from flask_login import login_user
from flask import session
from db_baseOperation import execute_query
from flask import Flask
from flask_bcrypt import Bcrypt
from mod_db_user_management import get_user_by_id

# Initialize Bcrypt
bcrypt = Bcrypt(flask_app)
flask_app.bcrypt = bcrypt

@pytest.fixture(scope='session')
def app():
    flask_app.config.update({
        "TESTING": True,
        # other configurations for testing
    })
    yield flask_app

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def user():
    user_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com',
        'password_hash': bcrypt.generate_password_hash('password123').decode('utf-8'),
        'role_id': 2
    }
    user_id = create_user(**user_data)
    user_data['UserID'] = user_id
    return user_data

@pytest.fixture(scope='function')
@pytest.fixture(scope='function')
def admin():
    admin_data = {
        'first_name': 'Admin',
        'last_name': 'User',
        'email': 'admin@example.com',
        'password_hash': bcrypt.generate_password_hash('password123').decode('utf-8'),
        'role_id': 1
    }
    admin_id = create_user(**admin_data)
    admin_data['UserID'] = admin_id
    return admin_data

@pytest.fixture(scope='function')
def login_user(client, user):
    with client.session_transaction() as sess:
        sess['user_id'] = user['UserID']
        sess['role_id'] = user['role_id']
    yield
    # Clear session after test
    with client.session_transaction() as sess:
        sess.clear()

@pytest.fixture(scope='function')
def login_admin(client, admin):
    with client.session_transaction() as sess:
        sess['user_id'] = admin['UserID']
        sess['role_id'] = admin['role_id']
    yield
    # Clear session after test
    with client.session_transaction() as sess:
        sess.clear()

@pytest.fixture(scope='function', autouse=True)
def clear_database():
    # Code to clear the database
    yield
    # Code to clear the database again if needed

@pytest.fixture(scope='function')
def mock_db_connection(monkeypatch):
    def mock_execute_query(*args, **kwargs):
        # Mock implementation of execute_query
        pass
    monkeypatch.setattr('db_baseOperation.execute_query', mock_execute_query)