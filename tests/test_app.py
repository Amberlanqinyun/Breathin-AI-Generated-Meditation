import pytest
from conftest import app, login_user, login_admin
from db_baseOperation import execute_query
import io

@pytest.fixture(scope='function')
def login_user(client):
    """Fixture for logging in a test user."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # Assuming 1 is a valid user ID
        sess['role_id'] = 1  # Assuming 1 is a valid role ID for access
    yield
    # Clear session after test
    with client.session_transaction() as sess:
        sess.clear()
        

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Breathe In' in response.data

def test_prepare_meditation_post(client):
    response = client.post('/prepare_meditation', data={'user_input': 'I am feeling stressed'})
    assert response.status_code == 302  # Expecting a redirect

def test_meditation_end(client):
    response = client.get('/meditation_end')
    assert response.status_code == 200
    assert b'Meditation Completed' in response.data

def test_select_category_get(client):
    response = client.get('/select_category')
    print(response.data)  # Debugging line
    assert response.status_code == 200
    assert b'Choose a Style for Your Meditation' in response.data  # Updated expected text

def test_select_category_post(client):
    response = client.post('/select_category', data={'category_id': '1'})
    assert response.status_code == 302  # Expecting a redirect

def test_meditation_category(client):
    response = client.get('/meditation/1')
    assert response.status_code == 200
    assert b'Choose Your Meditation Session' in response.data

def test_meditation_details(client, login_user):
    login_user  # Ensure the user is logged in
    response = client.get('/meditation_details/1')
    print(response.data)  # Debugging line
    assert response.status_code == 302 # Expecting a redirect

def test_submit_feedback(client, login_user):
    login_user  # Ensure the user is logged in
    response = client.post('/submit_feedback', data={'meditation_id': '1', 'rating': '5', 'comments': 'Great session!'})
    assert response.status_code == 200  # Expecting a successful response

def test_admin_meditations_get(client, login_admin):
    login_admin  # Ensure the admin is logged in
    response = client.get('/admin/meditations')
    assert response.status_code == 200
    assert b'Manage Meditations' in response.data

def test_admin_meditations_post(client, login_admin):
    login_admin  # Ensure the admin is logged in
    response = client.post('/admin/meditations', data={
        'title': 'New Meditation',
        'description': 'A new meditation session',
        'audio_file_path': (io.BytesIO(b"fake audio data"), 'test.mp3')
    })
    assert response.status_code == 302  # Expecting a redirect


def test_admin_edit_meditation_post(client, login_admin):
    login_admin  # Ensure the admin is logged in
    response = client.post('/admin/meditation/1', data={
        'text_content': 'Updated Meditation',
        'audio_file_path': (io.BytesIO(b"fake audio data"), 'test.mp3')
    })
    assert response.status_code == 302  # Expecting a redirect

def test_admin_delete_meditation(client, login_admin):
    login_admin  # Ensure the admin is logged in
    response = client.post('/admin/meditation/delete/1')
    assert response.status_code == 302  # Expecting a redirect

def test_admin_categories_get(client, login_admin):
    login_admin  # Ensure the admin is logged in
    response = client.get('/admin/categories')
    assert response.status_code == 200
    assert b'Manage Categories' in response.data

def test_admin_categories_post(client, login_admin):
    login_admin  # Ensure the admin is logged in
    response = client.post('/admin/categories', data={'name': 'New Category', 'description': 'Description'})
    assert response.status_code == 302  # Expecting a redirect

def test_admin_edit_category_get(client, login_admin):
    login_admin  # Ensure the admin is logged in
    response = client.get('/admin/category/1')
    assert response.status_code == 200
    assert b'Edit Category' in response.data

def test_admin_users_get(client, login_admin):
    login_admin  # Ensure the admin is logged in
    response = client.get('/admin/users')
    assert response.status_code == 200
    assert b'Manage Users' in response.data
    

def test_admin_user_edit_post(client, login_admin):
    login_admin  # Ensure the admin is logged in

    response = client.post('/admin/user/1', data={'username': 'NewUsername', 'email': 'newemail@example.com', 'role': 'user'})
    assert response.status_code == 302  # Expecting a redirect



def test_create_user(app, mock_db_connection):
    """Test the creation of a new user using direct SQL queries."""
    with app.app_context():
        # Define query for inserting a user
        query = """
            INSERT INTO Users (FirstName, LastName, Email, PasswordHash,RoleID)
            VALUES (%s, %s, %s, %s,%s)
        """
        data = ('Test', 'User', 'test@example.com', 'password123',2)

        # Execute the query and retrieve the new user ID
        user_id = execute_query(query, data, is_insert=True)
        assert user_id is not None

        # Query to fetch the created user by ID
        fetch_user_query = "SELECT * FROM Users WHERE UserID = %s"
        user = execute_query(fetch_user_query, (user_id,), fetchone=True)

        assert user is not None
        assert user['FirstName'] == 'Test'
        assert user['Email'] == 'test@example.com'

