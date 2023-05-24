import getpass
from cmd2 import Cmd, with_argparser, ansi
import argparse
import requests
import os

USER_URL = "http://localhost:8888/api/v1/"
WORD_URL = "http://localhost:8889/api/v1/"


class OutputHandler:
    def __init__(self, cmd2_app):
        self.cmd2_app = cmd2_app

    def print_hello(self):
        _output = """Welcome to Don't Remember!

Login) Login [username]        
Signup) Signup [username]
        """

        self.cmd2_app.poutput(_output)

    def print_login_succeed(self, username):
        _output = """Login successful!"""
        self.cmd2_app.poutput(_output)

    def print_settings(self):
        _output = """Settings command"""
        self.cmd2_app.poutput(_output)

    def print_signup(self, username):
        _output = f"""Signed up with username: {username}"""
        self.cmd2_app.poutput(_output)

    def print_team(self):
        _output = """Team command"""
        self.cmd2_app.poutput(_output)

    def print_add(self):
        _output = """Add command"""
        self.cmd2_app.poutput(_output)

    def print_word(self, word_dict):
        """
        word_dict:
        {
            "word": "this is definition"
        }


        :param word_dict:
        :return:
        """
        os.system('cls' if os.name == 'nt' else 'clear')  # This line clears the screen

        print(f"Current word: {list(word_dict.keys())[0]}")
        print(f"Definition: {list(word_dict.values())[0]}")

    @staticmethod
    def print_help(self):
        _output = """Help command"""
        self.cmd2_app.poutput(_output)

    @staticmethod
    def color_red(self, text):
        return ansi.style(text, fg=ansi.Fg.RED)

    @staticmethod
    def bold(self, text):
        return ansi.style(text, bold=True)

    @staticmethod
    def italic(self, text):
        return ansi.style(text, italic=True)


class RequestHandler:
    @staticmethod
    def request_login(username, password):
        """
        :param username:
        :param password:
        :return:
        """
        response = requests.get('https://api.example.com/check_login',
                                params={'username': username, 'password': password})
        data = response.json()
        return data

    @staticmethod
    def request_signup(username, password):
        """
        :param username:
        :param password:
        :return:
        """
        response = requests.get('https://api.example.com/check_login',
                                params={'username': username, 'password': password})
        data = response.json()
        return data

    @staticmethod
    def request_team():
        """
        :param username:
        :param password:
        :return:
        """
        response = requests.get('https://api.example.com/check_login',
                                params={'username': username, 'password': password})
        data = response.json()
        return data


class AppShell(Cmd):
    def __init__(self):
        super().__init__()
        self.logged_in = False
        self.word_dict = {"word": "this is definition"}
        self.output_handler = OutputHandler(self)
        self.request_handler = RequestHandler()
        self.set_window_title("Don't Remember")
        self.prompt = "[Don't Remember] >> "

    def preloop(self):
        self.output_handler.print_hello()

    login_parser = argparse.ArgumentParser()
    login_parser.add_argument('username', type=str, help='Username to login')

    @with_argparser(login_parser)
    def do_login(self, args):
        """Login as user"""
        if self.logged_in:
            print("Already logged in")
            return

        # password = getpass.getpass(prompt='Password: ', stream=None)
        # response = requests.get('https://api.example.com/check_login', params={'username': args.username, 'password': password})
        # data = response.json()

        if True:
            self.logged_in = True
            print("Login successful")
            print(f"Current word: {list(self.word_dict.keys())[0]}")
            print(f"Definition: {list(self.word_dict.values())[0]}")
        else:
            print("Login failed")

    signup_parser = argparse.ArgumentParser()
    signup_parser.add_argument('username', type=str, help='Username for signup')

    @with_argparser(signup_parser)
    def do_signup(self, args):
        """Sign up as new user"""
        if self.logged_in:
            print("Already logged in")
            return

        password = getpass.getpass(prompt='Password: ', stream=None)
        print(f"Signed up with username: {args.username} and password: {password}")

    def do_settings(self, arg):
        """Settings command"""
        if not self.logged_in:
            print("You need to be logged in to access settings")
            return
        print("Settings command")

    def do_team(self, arg):
        """
        Team command, need to show graph 5.
        1. request xxx endpoitn and getxxx
        2. requet xx end adn xxx
        :param arg:
        :return:
        """
        if not self.logged_in:
            print("You need to be logged in to access team")
            return
        print("Team command")

    def do_add(self, arg):
        """Add command"""
        if not self.logged_in:
            print("You need to be logged in to use add")
            return
        print("Add command")


if __name__ == '__main__':
    app = AppShell()
    app.cmdloop()
