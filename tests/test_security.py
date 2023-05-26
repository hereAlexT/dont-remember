from base import user_endpoint, word_endpoint, token_expiration
import pytest
import requests
import time

@pytest.fixture(scope='session', autouse=True)
def api_token():
    global token
    if 'token' not in globals():
        # Perform the login request and retrieve the token
        login_url = user_endpoint + '/login'
        data = {
            'username': 'test',
            'password': 'test'
        }
        response = requests.post(login_url, json=data)
        
        # Check if the login request was successful
        if response.status_code == 404:
            signup_response = requests.post(user_endpoint + '/signup', json=data)
            assert signup_response.status_code == 200, f"Signup request failed with status code {signup_response.status_code}"

            response = requests.post(login_url, json=data)

        assert response.status_code == 200, f"Login request failed with status code {response.status_code}"
        
        # Retrieve the token from the response
        token = response.json().get('token')
        assert token is not None, "Token not found in the login response"
    
    yield token


def test_add_new_word(api_token):
    # Use the token to add a new word through the API
    api_url = word_endpoint + '/add_new_word' 
    headers = {
        'Authorization': f'Bearer {api_token}'
    }
    payload = {
        'word': 'ahorse'
    }
    response = requests.post(api_url, headers=headers, json=payload)
    print(api_url, response.status_code)
    # Check if the request was successful
    assert response.status_code != 401, "API request failed with status code 401 (Unauthorized)"
    
def test_next_word(api_token):
    # Use the token to add a new word through the API
    api_url = word_endpoint + '/next_word' 
    headers = {
        'Authorization': f'Bearer {api_token}'
    }
    response = requests.get(api_url, headers=headers)
    print(api_url, response.status_code)    
    # Check if the request was successful
    assert response.status_code != 401, "API request failed with status code 401 (Unauthorized)"

def test_update_word(api_token):
    # Use the token to add a new word through the API
    api_url = word_endpoint + '/update_word'
    headers = {
        'Authorization': f'Bearer {api_token}'
    }
    payload = {
        'word': 'ahorse',
        'result': 'forget'
    }
    response = requests.put(api_url, headers=headers, json=payload)
    print(api_url, response.status_code)
    # Check if the request was successful
    assert response.status_code != 401, "API request failed with status code 401 (Unauthorized)"

def test_word_history(api_token):
    # Use the token to add a new word through the API
    api_url = word_endpoint + '/word_history'
    headers = {
        'Authorization': f'Bearer {api_token}'
    }
    response = requests.get(api_url, headers=headers)
    print(api_url, response.status_code)
    # Check if the request was successful
    assert response.status_code != 401, "API request failed with status code 401 (Unauthorized)"

def test_add_new_word_without_token():
    # Make a request to add a new word to the API without a token
    api_url = word_endpoint + '/add_new_word' 
    payload = {
        'word': 'ahorse'
    }
    response = requests.post(api_url, json=payload)
    print(api_url, response.status_code)
    # Check if the request returned a 401 status code (Unauthorized)
    assert response.status_code == 401, "API request without token did not return status code 401"

def test_next_word_without_token():
    # Make a request to add a new word to the API without a token
    api_url = word_endpoint + '/next_word' 
    response = requests.get(api_url)
    print(api_url, response.status_code)
    
    # Check if the request returned a 401 status code (Unauthorized)
    assert response.status_code == 401, "API request without token did not return status code 401"

def test_update_word_without_token():
    # Make a request to add a new word to the API without a token
    api_url = word_endpoint + '/update_word' 
    payload = {
        'word': 'ahorse',
        'result': 'forget'
    }
    response = requests.put(api_url, json=payload)
    print(api_url, response.status_code)
    
    # Check if the request returned a 401 status code (Unauthorized)
    assert response.status_code == 401, "API request without token did not return status code 401"

def test_word_history_without_token():
    # Make a request to add a new word to the API without a token
    api_url = word_endpoint + '/word_history' 
    response = requests.get(api_url)
    print(api_url, response.status_code)
    
    # Check if the request returned a 401 status code (Unauthorized)
    assert response.status_code == 401, "API request without token did not return status code 401"

def test_token_expiration(api_token):
    time.sleep(token_expiration)
    headers = {
        'Authorization': f'Bearer {api_token}'
    }
    word = {
        'word': 'ahorse'
    }
    response = requests.post(word_endpoint + '/add_new_word' , headers=headers, json=word)
    assert response.status_code == 401, "API request without token did not return status code 401"

    response = requests.get(word_endpoint + '/next_word' , headers=headers)
    assert response.status_code == 401, "API request without token did not return status code 401"

    update = {
        'word': 'ahorse',
        'result': 'forget'
    }
    response = requests.put(word_endpoint + '/update_word', headers=headers, json=update)
    assert response.status_code == 401, "API request without token did not return status code 401"

    response = requests.get(word_endpoint + '/word_history', headers=headers, json=update)
    assert response.status_code == 401, "API request without token did not return status code 401"




    