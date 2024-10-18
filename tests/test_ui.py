from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import app, login_user,login_admin

def test_invalid_meditation_id(client):
    response = client.get('/meditation/9999')  
    assert response.status_code == 302

def test_valid_meditation_page(client):
    response = client.get('/meditation/1')  
    assert response.status_code == 200

def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_login_functionality(client):
    response = client.post('/login', data={
        'email': 'testuser@example.com',  # Correct form key
        'password': 'testpass'
    })
    assert response.status_code == 302  # Expecting a redirect after successful login
    assert response.headers['Location'] == '/enter_password'  # Adjust as per logic


def test_logout_functionality(client, login_user):
    response = client.get('/logout')
    assert response.status_code == 302  # Assuming a redirect on successful logout
    assert '/login' in response.headers['Location']

def test_dashboard_access_without_login(client):
    response = client.get('/dashboard')
    assert response.status_code == 302  # Assuming a redirect to login page
    assert '/' in response.headers['Location']

def test_dashboard_access_with_login(client, login_user):
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Dashboard' in response.data