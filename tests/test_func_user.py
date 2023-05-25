# unit test for functionality test
from base import user_endpoint, word_endpoint
import unittest
import pytest
import requests
import uuid
import string
import random


class TestUser(unittest.TestCase):

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
        username = TestUser.generate_random_string(10)
        password = TestUser.generate_random_string(10)
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

    @staticmethod
    def next_word(token):
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(word_endpoint + '/next_word', headers=headers)
        print(response.json())
        assert response.status_code == 200, f"Next word failed with status code {response.status_code}"
        return response.json()['word']

    @staticmethod
    def update_word(token, word, result="remember"):
        headers = {
            "Authorization": f"Bearer {token}"
        }
        payload = {
            "word": word,
            "result": result
        }
        response = requests.put(word_endpoint + '/update_word', headers=headers, json=payload)
        print(response.json())
        assert response.status_code == 200, f"Update word failed with status code {response.status_code}"

    # create a pytest test that checks the user_endpoint with /health, expecting a 200 response
    def test_user_health(self):
        response = requests.get(user_endpoint + '/health')
        assert response.status_code == 200, f"User health check failed with status code {response.status_code}"

    def test_user_signup(self):
        """
        :return:
        """
        data = {
            "username": self.generate_random_string(10),
            "password": self.generate_random_string(10),
        }
        response = requests.post(user_endpoint + '/signup', json=data)
        assert response.status_code == 200, f"User signup failed with status code {response.status_code}"

    def test_user_signup_duplicate(self):
        """
        :return:
        """
        data = {
            "username": self.generate_random_string(10),
            "password": self.generate_random_string(10),
        }
        response = requests.post(user_endpoint + '/signup', json=data)
        assert response.status_code == 200, f"User signup failed with status code {response.status_code}"
        response = requests.post(user_endpoint + '/signup', json=data)
        assert response.status_code == 409, f"User signup duplicate failed with status code {response.status_code}"

    def test_user_missing_username(self):
        """
        :return:
        """
        data = {
            "password": self.generate_random_string(10)
        }
        response = requests.post(user_endpoint + '/signup', json=data)
        assert response.status_code == 400, f"User signup missing username failed with status code {response.status_code}"

    def test_user_missing_password(self):
        """
        :return:
        """
        data = {
            "username": self.generate_random_string(10)
        }
        response = requests.post(user_endpoint + '/signup', json=data)
        assert response.status_code == 400, f"User signup missing password failed with status code {response.status_code}"

    def test_user_missing_username_password(self):
        """
        :return:
        """
        data = {}
        response = requests.post(user_endpoint + '/signup', json=data)
        assert response.status_code == 400, f"User signup missing username and password failed with status code {response.status_code}"

    def test_user_more_than_username_password(self):
        """
        todo: what code need to be returned?
        :return:
        """
        data = {
            "username": self.generate_random_string(10),
            "password": self.generate_random_string(10),
            "extra": "extra"
        }
        response = requests.post(user_endpoint + '/signup', json=data)
        assert response.status_code == 200, f"User signup more than username and password failed with status code {response.status_code}"

    def test_user_login(self):
        """
        sign up a new user then login with the same credentials
        :return:
        """
        data = {
            "username": self.generate_random_string(10),
            "password": self.generate_random_string(10),
        }
        response = requests.post(user_endpoint + '/signup', json=data)
        assert response.status_code == 200, f"User signup failed with status code {response.status_code}"
        response = requests.post(user_endpoint + '/login', json=data)
        assert response.status_code == 200, f"User login failed with status code {response.status_code}"

    def test_user_login_wrong_password(self):
        """
        sign up a new user then login with the same credentials
        :return:
        """
        data = {
            "username": self.generate_random_string(10),
            "password": self.generate_random_string(10)
        }
        response = requests.post(user_endpoint + '/signup', json=data)
        assert response.status_code == 200, f"User signup failed with status code {response.status_code}"
        data["password"] = "wrong_password"
        response = requests.post(user_endpoint + '/login', json=data)
        assert response.status_code == 401, f"User login failed with status code {response.status_code}"

    def test_new_team(self):
        """
        request user_endpoint
        :return:
        """
        # signup
        data = {
            "username": self.generate_random_string(10),
            "password": self.generate_random_string(10)
        }

        print(data)

        response = requests.post(user_endpoint + '/signup', json=data)
        assert response.status_code == 200, f"User signup failed with status code {response.status_code}"
        # login
        response = requests.post(user_endpoint + '/login', json=data)
        assert response.status_code == 200, f"User login failed with status code {response.status_code}"
        # get the token form login response
        token = response.json()["token"]
        print(response.json())

        # use the endpoint /token_verify to verify the token. The token is bearer token.
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.post(user_endpoint + '/token_verify', headers=headers)
        print(response)
        assert response.status_code == 200, f"User token_verify failed with status code {response.status_code}"
        # create a new team
        data = {
            "name": self.generate_random_string(10),
            "plan": 10
        }
        response = requests.post(user_endpoint + '/new_team', headers=headers, json=data)
        assert response.status_code == 200, f"User new_team failed with status code {response.status_code}"

        # add the current user to team by endpoint /add_me_to_team, it should return 400
        response = requests.post(user_endpoint + '/add_me_to_team', headers=headers)
        assert response.status_code == 400, f"User add_me_to_team failed with status code {response.status_code}"

    def test_add_new_user_to_team(self):
        """
        1. add a new user
        2. build a new team
        3. add another new user
        4. add the new user to the team (should return 200)
        5. leave a team
        :return:
        """
        # add a new user
        user_1 = {
            "username": self.generate_random_string(10),
            "password": self.generate_random_string(10)
        }
        response = requests.post(user_endpoint + '/signup', json=user_1)
        assert response.status_code == 200, f"User signup failed with status code {response.status_code}"
        # login
        response = requests.post(user_endpoint + '/login', json=user_1)
        assert response.status_code == 200, f"User login failed with status code {response.status_code}"
        # get the token form login response
        token_1 = response.json()["token"]
        # create a new team by user_1
        headers = {
            "Authorization": f"Bearer {token_1}",
        }
        data = {
            "name": self.generate_random_string(10),
            "plan": 10
        }
        response = requests.post(user_endpoint + '/new_team', headers=headers, json=data)
        assert response.status_code == 200, f"User new_team failed with status code {response.status_code}"
        # get the team uuid from response
        team_uuid = response.json()["team_uuid"]

        # create another user
        user_2 = {
            "username": self.generate_random_string(10),
            "password": self.generate_random_string(10)
        }
        response = requests.post(user_endpoint + '/signup', json=user_2)
        assert response.status_code == 200, f"User signup failed with status code {response.status_code}"
        # login
        response = requests.post(user_endpoint + '/login', json=user_2)
        assert response.status_code == 200, f"User login failed with status code {response.status_code}"
        # get the token form login response
        token_2 = response.json()["token"]

        # add user_2 to the team, it should return 200
        headers = {
            "Authorization": f"Bearer {token_2}"
        }
        payload = {
            "team_uuid": team_uuid
        }
        response = requests.post(user_endpoint + '/add_me_to_team', headers=headers, json=payload)
        # print response
        print(response.json())
        assert response.status_code == 200, f"User add_me_to_team failed with status code {response.status_code}"

        # leave the team
        response = requests.post(user_endpoint + '/leave_team', headers=headers, json={"team_uuid": team_uuid})
        print(response.json())
        assert response.status_code == 200, f"User leave_team failed with status code {response.status_code}"

        # get team info should return
        response = requests.get(user_endpoint + '/team_info', headers=headers)
        assert response.status_code == 400, f"User team_info failed with status code {response.status_code}"

    def test_update_team(self):
        """
        1. create a user
        2. login
        2. create a team
        3. update team with correct data

        :param self:
        :return:
        """
        # signup a user
        user = {
            "username": self.generate_random_string(10),
            "password": self.generate_random_string(10)
        }
        response = requests.post(user_endpoint + '/signup', json=user)
        assert response.status_code == 200, f"User signup failed with status code {response.status_code}"
        # login
        response = requests.post(user_endpoint + '/login', json=user)
        assert response.status_code == 200, f"User login failed with status code {response.status_code}"
        # get the token form login response
        token_1 = response.json()["token"]
        # create a new team by user_1
        headers_1 = {
            "Authorization": f"Bearer {token_1}",
        }
        data = {
            "name": self.generate_random_string(10),
            "plan": 10
        }
        response = requests.post(user_endpoint + '/new_team', headers=headers_1, json=data)
        assert response.status_code == 200, f"User new_team failed with status code {response.status_code}"
        # get the team uuid from response
        team_uuid = response.json()["team_uuid"]

        # update with new plan as 30
        data = {
            "team_uuid": team_uuid,
            "plan": 30
        }
        response = requests.post(user_endpoint + '/update_team', headers=headers_1, json=data)
        print(response.json())
        assert response.status_code == 200, f"User update_team failed with status code {response.status_code}"

        # get team info, to check if the plan is updated
        response = requests.get(user_endpoint + '/team_info', headers=headers_1)
        assert response.status_code == 200, f"User team_info failed with status code {response.status_code}"
        assert response.json()["plan"] == 30, f"User team_info failed with status code {response.status_code}"

    def test_user_progress(self):
        """
        visit the endpoint \personal_progress it should show 200 with peronal progres
        :return:
        """
        # create a user and login
        username, password = TestUser.create_user()
        token = TestUser.login(username, password)
        headers = {
            "Authorization": f"Bearer {token}"
        }
        # get the personal progress
        response = requests.get(user_endpoint + '/personal_progress', headers=headers)
        print(response.json())
        assert response.status_code == 200, f"User personal_progress failed with status code {response.status_code}"
        # the return json should has a status==200, the studied_today which is 0 and plan which is 20
        assert response.json()[
                   "status"] == 200, f"User personal_progress failed with status code {response.status_code}"
        assert response.json()[
                   "studied_today"] == 0, f"User personal_progress failed with status code {response.status_code}"
        assert response.json()["plan"] == 20, f"User personal_progress failed with status code {response.status_code}"

        _words = ["hello", "world", "good", "job", "excellent", "nice", "reference", "model", "algorithm", "happy"]
        for w in _words:
            TestUser.add_new_word(token, w)
        response = requests.get(user_endpoint + '/personal_progress', headers=headers)
        assert response.status_code == 200, f"User personal_progress failed with status code {response.status_code}"
        # the return json should has a status==200, the studied_today which is 0 and plan which is 20
        assert response.json()[
                   "status"] == 200, f"User personal_progress failed with status code {response.status_code}"
        assert response.json()[
                   "studied_today"] == 0, f"User personal_progress failed with status code {response.status_code}"
        print(response.json())
        # visit next word endpoint for 3 times
        for i in range(3):
            word = TestUser.next_word(token)
            TestUser.update_word(token, word, "remember")
        word = TestUser.next_word(token)
        TestUser.update_word(token, word, "forget")

        # check the progress again
        response = requests.get(user_endpoint + '/personal_progress', headers=headers)
        print(response.json())
        assert response.status_code == 200, f"User personal_progress failed with status code {response.status_code}"
        # the return json should has a status==200, the studied_today which is 0 and plan which is 20
        assert response.json()[
                   "status"] == 200, f"User personal_progress failed with status code {response.status_code}"
        assert response.json()[
                   "studied_today"] == 4, f"User personal_progress failed with status code {response.status_code}"

    def test_team_info(self):
        """
        1. create a user as user_1 and login with token_1
        2. create team
        3. create another user as user_2 and login with token_2
        4. add user_2 to team
        5. learn 2 words by user_2
        6. check team info by user_1
        :return:
        """
        # create user_1
        username_1, password_1 = TestUser.create_user()
        token_1 = TestUser.login(username_1, password_1)
        # create user_2
        username_2, password_2 = TestUser.create_user()
        token_2 = TestUser.login(username_2, password_2)

        # create team by user_1
        headers_1 = {
            "Authorization": f"Bearer {token_1}"
        }
        data = {
            "name": self.generate_random_string(10),
            "plan": 10
        }
        response = requests.post(user_endpoint + '/new_team', headers=headers_1, json=data)
        assert response.status_code == 200, f"User new_team failed with status code {response.status_code}"
        # get the team uuid from response
        team_uuid = response.json()["team_uuid"]

        # add user_2 to team
        headers_2 = {
            "Authorization": f"Bearer {token_2}"
        }
        data = {
            "team_uuid": team_uuid
        }
        response = requests.post(user_endpoint + '/add_me_to_team', headers=headers_2, json=data)
        print(response)
        assert response.status_code == 200, f"User join_team failed with status code {response.status_code}"

        # add 10 words to user_2
        _words = ["hello", "world", "good", "job", "excellent", "nice", "reference", "model", "algorithm", "happy"]
        for w in _words:
            TestUser.add_new_word(token_2, w)

        # learn 2 words by user_2
        for i in range(2):
            word = TestUser.next_word(token_2)
            TestUser.update_word(token_2, word, "remember")

        # get team_info
        response = requests.get(user_endpoint + '/team_info', headers=headers_1)
        print(response.json())
