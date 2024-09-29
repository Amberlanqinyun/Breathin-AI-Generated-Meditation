import pytest
from flask import json

def test_chat_ai_endpoint(client):
    response = client.post('/chat', json={'message': 'I need help'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'response' in data

def test_meditation_api_endpoints(client, login_user):
    # Test GET /meditation/<id>
    response = client.get('/meditation/1')
    assert response.status_code == 200
    assert b'Choose Your Meditation Session' in response.data

    # Test POST /meditation/<id>
    response = client.post('/meditation/1', data={'duration': '10'})
    assert response.status_code == 302  # Expecting a redirect

# Add more API tests for other endpoints