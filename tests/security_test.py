import pytest
import requests

def pytest_namespace():
    return {'localhost_user', 'http://127.0.0.1:8888/'}

@pytest.fixture
def api_token():
    # Perform the login request and retrieve the token
    login_url = localhost_user + 'login' 
    data = {
        'username': 'test',
        'password': 'test'
    }
    response = requests.post(login_url, json=data)
    
    # Check if the login request was successful
    if response.status_code == 404:
        signup_response = response.post(localhost_user + 'signup', json=data)
        assert signup_response.status_code == 200, f"Signup request failed with status code {signup_response.status_code}"

        response = requests.post(login_url, json=data)

    assert response.status_code == 200, f"Login request failed with status code {response.status_code}"
    
    # Retrieve the token from the response
    token = response.json().get('token')
    assert token is not None, "Token not found in the login response"
    
    yield token

def test_add_new_word(api_token):
    # Use the token to add a new word through the API
    api_url = localhost_user + 'add_new_word' 
    headers = {
        'Authorization': f'Bearer {api_token}'
    }
    payload = {
        'word': 'ahorse'
    }
    response = requests.post(api_url, headers=headers, json=payload)
    
    # Check if the request was successful
    assert response.status_code != 401, "API request failed with status code 401 (Unauthorized)"
    # Add additional assertions or checks here as needed

def test_add_new_word_without_token():
    # Make a request to add a new word to the API without a token
    api_url = localhost_user + 'add_new_word' 
    payload = {
        'word': 'ahorse'
    }
    response = requests.post(api_url, json=payload)
    
    # Check if the request returned a 401 status code (Unauthorized)
    assert response.status_code == 401, "API request without token did not return status code 401"
    # Add additional assertions or checks here as needed