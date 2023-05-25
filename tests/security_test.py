import pytest
import requests

pytest.localhost_user = 'http://127.0.0.1:8888/api/v1/'
pytest.localhost_word = 'http://127.0.0.1:8889/api/v1/'
pytest.token = ''

@pytest.fixture(scope='session', autouse=True)
def api_token():
    global token
    if 'token' not in globals():
        # Perform the login request and retrieve the token
        login_url = pytest.localhost_user + 'login'
        data = {
            'username': 'test',
            'password': 'test'
        }
        response = requests.post(login_url, json=data)
        
        # Check if the login request was successful
        if response.status_code == 404:
            signup_response = request.post(pytest.localhost_user + 'signup', json=data)
            assert signup_response.status_code == 200, f"Signup request failed with status code {signup_response.status_code}"

            response = requests.post(login_url, json=data)

        assert response.status_code == 200, f"Login request failed with status code {response.status_code}"
        
        # Retrieve the token from the response
        token = response.json().get('token')
        assert token is not None, "Token not found in the login response"
    
    yield token


def test_add_new_word(api_token):
    # Use the token to add a new word through the API
    api_url = pytest.localhost_word + 'add_new_word' 
    headers = {
        'Authorization': f'Bearer {api_token}'
    }
    payload = {
        'word': 'ahorse'
    }
    response = requests.post(api_url, headers=headers, json=payload)
    print(response.status_code)
    # Check if the request was successful
    assert response.status_code != 401, "API request failed with status code 401 (Unauthorized)"
    
def test_next_word(api_token):
    # Use the token to add a new word through the API
    api_url = pytest.localhost_word + 'next_word' 
    headers = {
        'Authorization': f'Bearer {api_token}'
    }
    response = requests.get(api_url, headers=headers)
    print(response.status_code)
    print(api_url)
    # Check if the request was successful
    assert response.status_code != 401, "API request failed with status code 401 (Unauthorized)"

def test_update_word(api_token):
    # Use the token to add a new word through the API
    api_url = pytest.localhost_word + 'update_word'
    headers = {
        'Authorization': f'Bearer {api_token}'
    }
    response = requests.post(api_url, headers=headers)
    print(response.status_code)
    # Check if the request was successful
    assert response.status_code != 401, "API request failed with status code 401 (Unauthorized)"

def test_word_history(api_token):
    # Use the token to add a new word through the API
    api_url = pytest.localhost_word + 'word_history'
    headers = {
        'Authorization': f'Bearer {api_token}'
    }
    response = requests.post(api_url, headers=headers)
    print(response.status_code)
    # Check if the request was successful
    assert response.status_code != 401, "API request failed with status code 401 (Unauthorized)"

def test_add_new_word_without_token():
    # Make a request to add a new word to the API without a token
    api_url = pytest.localhost_word + 'add_new_word' 
    payload = {
        'word': 'ahorse'
    }
    response = requests.post(api_url, json=payload)
    
    # Check if the request returned a 401 status code (Unauthorized)
    assert response.status_code == 401, "API request without token did not return status code 401"
    