import pytest
from conftest import app
import io


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Breathe In' in response.data

def test_prepare_meditation_get(client):
    response = client.get('/prepare_meditation')
    print(response.data)  # Debugging line
    assert response.status_code == 200
    assert b'Start meditation' in response.data

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
    assert response.status_code == 200
    assert b'Meditation Details' in response.data

def test_submit_feedback(client, login_user):
    login_user  # Ensure the user is logged in
    response = client.post('/submit_feedback', data={'feedback': 'Great session!'})
    print(response.data)  # Debugging line
    assert response.status_code == 302  # Expecting a redirect

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

def test_admin_edit_meditation_get(client, login_admin):
    login_admin  # Ensure the admin is logged in
    response = client.get('/admin/meditation/1')
    assert response.status_code == 200
    assert b'Edit Meditation' in response.data
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