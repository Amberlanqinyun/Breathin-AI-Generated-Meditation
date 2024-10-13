import pytest
import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_baseOperation import execute_query

def test_create_user(app, mock_db_connection):
    """Test the creation of a new user using direct SQL queries."""
    with app.app_context():
        # Define query for inserting a user
        query = """
            INSERT INTO Users (FirstName, LastName, Email, PasswordHash)
            VALUES (%s, %s, %s, %s)
        """
        data = ('Test', 'User', 'test@example.com', 'password123')

        # Execute the query and retrieve the new user ID
        user_id = execute_query(query, data, is_insert=True)
        assert user_id is not None

        # Query to fetch the created user by ID
        fetch_user_query = "SELECT * FROM Users WHERE UserID = %s"
        user = execute_query(fetch_user_query, (user_id,), fetchone=True)

        assert user is not None
        assert user['FirstName'] == 'Test'
        assert user['Email'] == 'test@example.com'

def test_create_meditation_session(app, mock_db_connection, login_user):
    """Test the creation of a new meditation session."""
    with app.app_context():
        # Define query for inserting a meditation session
        query = """
            INSERT INTO MeditationSessions (UserID, CategoryID, Duration, Completed)
            VALUES (%s, %s, %s, %s)
        """
        data = (login_user['UserID'], 1, 10, True)

        # Execute the query and retrieve the new session ID
        session_id = execute_query(query, data, is_insert=True)
        assert session_id is not None

        # Query to fetch the created session by ID
        fetch_session_query = "SELECT * FROM MeditationSessions WHERE SessionID = %s"
        session = execute_query(fetch_session_query, (session_id,), fetchone=True)

        assert session is not None
        assert session['UserID'] == login_user['UserID']
        assert session['CategoryID'] == 1
        assert session['Duration'] == 10
        assert session['Completed'] == True
