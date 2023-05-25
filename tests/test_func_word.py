# unit test for functionality test
from base import user_endpoint, word_endpoint
import unittest
import pytest
import requests
import uuid
import string
import random
import nltk
from nltk.corpus import words

nltk.download('words')


class TestWord(unittest.TestCase):

    @staticmethod
    def generate_random_string(length):
        # Combine all the characters we want to use
        characters = string.ascii_letters + string.digits
        # Use a list comprehension to generate a list of 'length' random characters
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string

    @staticmethod
    def create_user():
        # create a random username and password
        username = TestWord.generate_random_string(10)
        password = TestWord.generate_random_string(10)
        # create a new user
        response = requests.post(user_endpoint + '/signup', json={
            "username": username,
            "password": password
        })
        assert response.status_code == 200, f"User creation failed with status code {response.status_code}"
        return username, password

    @staticmethod
    def login(username, password):
        """ login and return token"""
        response = requests.post(user_endpoint + '/login', json={
            "username": username,
            "password": password
        })
        assert response.status_code == 200, f"User login failed with status code {response.status_code}"
        return response.json()['token']

    @staticmethod
    def add_new_word(token, word="hello"):
        payload = {
            "word": word
        }
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.post(word_endpoint + '/add_new_word', json=payload, headers=headers)
        print(response.json())
        assert response.status_code == 200, f"Add new word failed with status code {response.status_code}"
        return 200

    # create a pytest test that checks the user_endpoint with /health, expecting a 200 response
    def test_word_health(self):
        response = requests.get(word_endpoint + '/health')
        assert response.status_code == 200, f"User health check failed with status code {response.status_code}"

    def test_add_new_word(self):
        """
        1. signup and login
        2. add a new word
        3. visit word_history to check if the word exist
        :return:
        """
        # signup and login
        username, password = TestWord.create_user()
        token = TestWord.login(username, password)

        # add a new word
        word = "hello"
        payload = {
            "word": word
        }
        print(payload)
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.post(word_endpoint + '/add_new_word', json=payload, headers=headers)
        assert response.status_code == 200, f"Add new word failed with status code {response.status_code}"

        # visit word_history to check if the word exist
        response = requests.get(word_endpoint + '/word_history', headers=headers)
        print(response.json())
        assert response.status_code == 200, f"Get word history failed with status code {response.status_code}"
        assert response.json()['history'][0][
                   'word'] == word, f"Get word history failed with status code {response.status_code}"

    def test_update_word(self):
        """
        1. signup and login
        2. add a new word
        3. update the word
        :return:
        """
        # signup and login
        username, password = TestWord.create_user()
        token = TestWord.login(username, password)
        # add new word
        word = "hello"
        TestWord.add_new_word(token, word)
        # update the word
        payload = {
            "word": word,
            "result": "remember"
        }
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.post(word_endpoint + '/update_word', json=payload, headers=headers)
        print(response.json())
        assert response.status_code == 200, f"Update word failed with status code {response.status_code}"

    def test_word_history(self):
        """
        1. signup and login
        2. add 10 new word
        3. visit word_history to check if the word exist
        :return:
        """
        # signup and login
        username, password = TestWord.create_user()
        token = TestWord.login(username, password)
        # add 10 new word
        _words = ["hello", "world", "good", "job", "excellent", "nice", "reference", "model", "algorithm", "happy"]
        for w in _words:
            TestWord.add_new_word(token, w)
        # visit word_history to check if the word exist
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(word_endpoint + '/word_history', headers=headers)
        print(response.json())
        assert response.status_code == 200, f"Get word history failed with status code {response.status_code}"
        assert len(response.json()['history']) == 10, f"Get word history failed with status code {response.status_code}"

    def test_next_word(self):
        """
        1. create signup / login
        2. add 1 word
        3. use next_word endpoint, it should return the word just added
        :return:
        """
        # signup and login
        username, password = TestWord.create_user()
        token = TestWord.login(username, password)
        # add 1 word
        word = "hello"
        TestWord.add_new_word(token, word)
        # use next_word endpoint, it should return the word just added
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(word_endpoint + '/next_word', headers=headers)
        # print response content
        print(response.json())
        assert response.status_code == 200, f"Get next word failed with status code {response.status_code}"
        assert response.json()['word'] == word, f"Get next word failed with status code {response.status_code}"
