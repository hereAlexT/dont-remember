import getpass
from cmd2 import Cmd, with_argparser
import argparse
import requests


def print_login(username):
    print(f"Logged in with username: {username}")


def print_settings():
    print("Settings command")


def print_signup(username):
    print(f"Signed up with username: {username}")


def print_team():
    print("Team command")


def print_add():
    print("Add command")


def print_word(word_dict):
    """
    word_dict:
    {
        "word": "this is definition"
    }


    :param word_dict:
    :return:
    """
    print(f"Current word: {list(word_dict.keys())[0]}")
    print(f"Definition: {list(word_dict.values())[0]}")


class AppShell(Cmd):
    def __init__(self):
        super().__init__()
        self.logged_in = False
        self.word_dict = {"word": "this is definition"}

    def preloop(self):
        print("""
Don't Remember
login) Login
signup) Signup
        """)

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
