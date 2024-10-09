import pytest
import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mod_db_account import db

def test_create_user(app, mock_db_connection):
    with app.app_context():
        user_id = db.create_user(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password_hash='password123'
        )
        assert user_id is not None

        user = db.get_user_by_id(user_id)
        assert user['FirstName'] == 'Test'
        assert user['Email'] == 'test@example.com'

def test_create_meditation_session(app, mock_db_connection, login_user):
    with app.app_context():
        session_data = {
            'user_id': login_user['UserID'],
            'category_id': 1,
            'duration': 10,
            'completed': True
        }
        session_id = db.create_meditation_session(session_data)
        assert session_id is not None

        session = db.get_meditation_session(session_id)
        assert session['user_id'] == login_user['UserID']
        assert session['category_id'] == 1
        assert session['duration'] == 10
        assert session['completed'] == True