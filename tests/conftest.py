import sys
import os
import pytest
from flask import session
from flask_bcrypt import Bcrypt


# Add the correct directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import the app
from app import app as flask_app
from mod_db_account import create_user, hash_password
from db_baseOperation import execute_query

# Initialize Bcrypt
bcrypt = Bcrypt(flask_app)
flask_app.bcrypt = bcrypt




@pytest.fixture(scope='session')
def app():
    # Update the app configuration for testing
    flask_app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,  # Disable CSRF for testing
    })

    yield flask_app

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def user():
    """Fixture for creating a test user."""
    user_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': f'test{os.urandom(4).hex()}@example.com',  # Ensure unique email
        'password_hash': bcrypt.generate_password_hash('password123').decode('utf-8'),
        'role_id': 2
    }
    
    # Insert user into the database using PyMySQL
    query = """
        INSERT INTO Users (FirstName, LastName, Email, PasswordHash, RoleID)
        VALUES (%s, %s, %s, %s, %s)
    """
    data = (user_data['first_name'], user_data['last_name'], user_data['email'], user_data['password_hash'], user_data['role_id'])
    
    user_id = execute_query(query, data, is_insert=True)
    user_data['UserID'] = user_id
    return user_data

@pytest.fixture(scope='function')
def admin():
    """Fixture for creating a test admin user."""
    admin_data = {
        'first_name': 'Admin',
        'last_name': 'User',
        'email': f'admin{os.urandom(4).hex()}@example.com',  # Ensure unique email
        'password_hash': bcrypt.generate_password_hash('password123').decode('utf-8'),
        'role_id': 1
    }
    
    # Insert admin into the database using PyMySQL
    query = """
        INSERT INTO Users (FirstName, LastName, Email, PasswordHash, RoleID)
        VALUES (%s, %s, %s, %s, %s)
    """
    data = (admin_data['first_name'], admin_data['last_name'], admin_data['email'], admin_data['password_hash'], admin_data['role_id'])
    
    admin_id = execute_query(query, data, is_insert=True)
    admin_data['UserID'] = admin_id
    return admin_data

@pytest.fixture(scope='function')
def login_user(client, user):
    """Fixture for logging in a test user."""
    with client.session_transaction() as sess:
        sess['user_id'] = user['UserID']
        sess['role_id'] = user['role_id']
    yield
    # Clear session after test
    with client.session_transaction() as sess:
        sess.clear()

@pytest.fixture(scope='function')
def login_admin(client, admin):
    """Fixture for logging in a test admin."""
    with client.session_transaction() as sess:
        sess['user_id'] = admin['UserID']
        sess['role_id'] = admin['role_id']
    yield
    # Clear session after test
    with client.session_transaction() as sess:
        sess.clear()

@pytest.fixture(scope='function', autouse=True)
def clear_database():
    """Fixture for clearing the database before and after each test."""
    # Clear related tables first to avoid foreign key constraint errors
    execute_query("DELETE FROM Achievements")
    execute_query("DELETE FROM MeditationSessions")
    execute_query("DELETE FROM UserFeedback")
    execute_query("DELETE FROM Users")
    yield
    # Clear again after test to reset the database
    execute_query("DELETE FROM Achievements")
    execute_query("DELETE FROM MeditationSessions")
    execute_query("DELETE FROM UserFeedback")
    execute_query("DELETE FROM Users")

@pytest.fixture(scope='function')
def mock_db_connection(monkeypatch):
    """Fixture for mocking the database connection."""
    def mock_execute_query(*args, **kwargs):
        # Mock implementation of execute_query
        return None
    monkeypatch.setattr('db_baseOperation.execute_query', mock_execute_query)