import getpass
import logging

from cmd2 import Cmd, with_argparser
import argparse
import requests
import textwrap
from tabulate import tabulate

USER_ENDPOINT = 'http://dont-remember-123619125.us-east-1.elb.amazonaws.com/api/v1/users'
WORD_ENDPOINT = 'http://dont-remember-123619125.us-east-1.elb.amazonaws.com/api/v1/words'


class RequestHandler:

    def __init__(self, user_endpoint=USER_ENDPOINT, word_endpoint=WORD_ENDPOINT):
        self.token = None
        self.user_url = user_endpoint
        self.word_url = word_endpoint
        self.header = {}
        self.user_uuid = None
        self.team_uuid = None

    def get_header(self, token):
        if token is None:
            token = self.token
        return {
            "Authorization": f"Bearer {self.token}"
        }

    @staticmethod
    def check_users_connection():
        """
        check user and word service /health endpoint
        :return:
        """
        response = requests.get(USER_ENDPOINT + '/health')
        if response.status_code == 200:
            return True
        else:
            return False

    @staticmethod
    def check_words_connection():
        """
        check user and word service /health endpoint
        :return:
        """
        response = requests.get(WORD_ENDPOINT + '/health')
        if response.status_code == 200:
            return True
        else:
            return False

    @staticmethod
    def signup(username, password):
        """
        :param username:
        :param password:
        :return:
        """
        response = requests.post(USER_ENDPOINT + '/signup', json={
            "username": username,
            "password": password
        })
        return response.json()

    def login(self, username, password):
        """
        endpoint user /login
        :param username:
        :param password:
        :return:
        """
        response = requests.post(USER_ENDPOINT + '/login', json={
            "username": username,
            "password": password
        })
        # if response.status_code == 200, assign token
        if response.status_code == 200:
            self.token = response.json()['token']
            self.header = self.get_header(self.token)
        return response.json()

    def change_plan(self, plan):
        """
        endpoint user /set_personal_plan
        :param plan:
        :return:
        """
        response = requests.put(USER_ENDPOINT + '/change_plan', json={
            "plan": plan
        }, headers=self.header)
        return response.json()

    def new_team(self, name: str, plan: int = 20):
        """
        visit endpoint user /new_team
        :param plan:
        :param name:
        :return:
        """
        payload = {
            "name": name,
            "plan": plan
        }
        response = requests.post(USER_ENDPOINT + '/new_team', json=payload, headers=self.header)
        return response.json()

    def add_me_to_team(self, team_uuid):
        """
        visit endpoint user /add_me_to_team
        :param team_uuid:
        :return:
        """
        payload = {
            "team_uuid": team_uuid
        }
        response = requests.post(USER_ENDPOINT + '/add_me_to_team', json=payload, headers=self.header)
        return response.json()

    def leave_team(self, team_uuid):
        """
        visist user /leave team
        :param team_uuid:
        :return:
        """
        payload = {
            "team_uuid": team_uuid
        }

        response = requests.post(USER_ENDPOINT + '/leave_team', json=payload, headers=self.header)
        return response.json()

    def update_team(self, team_uuid, plan):
        """
        visit user /update_team
        :param plan:
        :param team_uuid:
        :return:
        """
        payload = {
            "team_uuid": team_uuid,
            "plan": plan
        }

        response = requests.post(USER_ENDPOINT + '/update_team', json=payload, headers=self.header)
        return response.json()

    def team_info(self):
        """
        visit user /team_info
        :return:
        """
        response = requests.get(USER_ENDPOINT + '/team_info', headers=self.header)
        return response.json()

    def personal_progress(self):
        """
        visit user /personal_progress
        :return:
        """
        response = requests.get(USER_ENDPOINT + '/personal_progress', headers=self.header)
        return response.json()

    def add_new_word(self, word):
        """
        endpoint word /add_new_word
        :param word:
        :return:
        """
        payload = {
            "word": word
        }
        response = requests.post(WORD_ENDPOINT + '/add_new_word', json=payload, headers=self.header)
        return response.json()

    def next_word(self):
        """
        visit endpoint user next_word
        :return:
        """

        response = requests.get(WORD_ENDPOINT + '/next_word', headers=self.header)
        return response.json()

    def update_word(self, word, result):
        """
        update word endpoint: word /update word
        method PUT
        :return:
        """
        payload = {
            "word": word,
            "result": result
        }
        response = requests.put(WORD_ENDPOINT + '/update_word', json=payload, headers=self.header)
        return response.json()

    def delete_word(self, word):
        """
        delete world endpoint: word /delete_word
        method POST
        :param word:
        :return:
        """
        payload = {
            "word": word
        }
        response = requests.post(WORD_ENDPOINT + '/delete_word', json=payload, headers=self.header)
        return response.json()

    def word_history(self):
        """
        visit endpoint word /word_history
        :return:
        """
        response = requests.get(WORD_ENDPOINT + '/word_history', headers=self.header)
        return response.json()


# Welcome Page
class OutputHandler:
    def __init__(self, cmd2_app):
        self.cmd2_app = cmd2_app
        self.clear_count = 0

    border_char = "*"
    box_width = 40
    box_top = border_char * box_width

    def print_hello(self):
        welcome_message = textwrap.fill("""Welcome to Don't Remember!""", self.box_width)
        command_message = textwrap.fill("""Use the following commands.""", self.box_width)

        login_message = "- login [username]"
        signup_message = "- signup [username]"
        help_message = "- help -v"

        # Make sure the messages are within the box width
        login_message = textwrap.fill(login_message, self.box_width)
        middle_border = self.border_char + " " * (self.box_width - 2) + self.border_char
        signup_message = textwrap.fill(signup_message, self.box_width)

        box_bottom = self.border_char * self.box_width

        # Concatenate all lines
        _output = "\n".join(
            [self.box_top, welcome_message, command_message, middle_border, login_message, signup_message, help_message,
             middle_border, box_bottom])

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
        word = word_dict["word"]
        meanings = word_dict["meanings"]

        # Prepare the header and footer
        header = f"{'-' * ((50 - len(word)) // 2)}-> \033[31m\033[1m{word}\033[0m <-{'-' * ((50 - len(word)) // 2)}"
        # 31 for red, 1 for bold

        # Start with the header
        _output = header

        for i, meaning in enumerate(meanings, 1):
            _output += f"\n{i}.\n"
            _output += f"\033[34m\033[3m{meaning['speech_part']}\033[0m\n"  # 34 for blue, 3 for italic
            _output += f"{meaning['definition']}\n"
            # add example, if it exists
            if "example" in meaning:
                _output += f"· {meaning['example']}\n"
            _output += "-" * len(header)  # Add the line separator
        _output += "\nUse command '\033[1m\033[3mupdateword remember\033[0m' or '\033[1m\033[3mupdateword forget\033[0m' to update the word."
        self.cmd2_app.poutput(_output)

    def print_learning_history(self, response):
        """
        response: {'history': [{'last_review_time': '...', 'next_review_time': '...', 'uuid': '...', 'word': '...'}]}
        """
        history = response['history']

        # Extract the data we care about into a list of dictionaries.
        history_data = [
            {'Word': h['word'], 'Last Review Time': h['last_review_time'], 'Next Review Time': h['next_review_time'],
             'UUID': h['uuid']} for h in history]

        # Use tabulate to create a table from the data. "pipe" is the table format.
        table = tabulate(history_data, headers="keys", tablefmt="pipe", showindex="always")

        # Print the table
        self.cmd2_app.poutput(table)

    from tabulate import tabulate

    def print_teaminfo(self, response):
        """
        response:
        {
            'plan': 20,
            'status': 200,
            'team_member': [{'studied_today': 1, 'username': 'b'}],
            'team_name': 'teng',
            'team_uuid': '00372df8-a100-4ee3-b58a-769baec93367'
        }
        """
        # Extract the data we care about into a list of dictionaries.
        member_data = [{'Username': m['username'], 'Studied Today': m['studied_today']} for m in
                       response['team_member']]

        # Use tabulate to create a table from the data. "pipe" is the table format.
        table = tabulate(member_data, headers="keys", tablefmt="pipe", showindex="always")

        # Print the team name, uuid, and table
        self.cmd2_app.poutput(f"Team Name: {response['team_name']}")
        self.cmd2_app.poutput(f"Team UUID: {response['team_uuid']}")
        self.cmd2_app.poutput(f"Plan: {response['plan']}")
        self.cmd2_app.poutput("\nMember Info:")
        self.cmd2_app.poutput(table)

    from tabulate import tabulate

    def print_team_info(self, response):
        """
        response:
        {
            'plan': 20,
            'status': 200,
            'team_member': [{'studied_today': 1, 'username': 'b'}],
            'team_name': 'teng',
            'team_uuid': '00372df8-a100-4ee3-b58a-769baec93367'
        }
        """
        # Extract the data we care about into a list of dictionaries.
        member_data = [{'Username': m['username'], 'Studied Today': m['studied_today']} for m in
                       response['team_member']]

        # Use tabulate to create a table from the data. "pipe" is the table format.
        table = tabulate(member_data, headers="keys", tablefmt="pipe", showindex="always")

        # Print the team name, uuid, and table
        self.cmd2_app.poutput(f"Team Name: {response['team_name']}")
        self.cmd2_app.poutput(f"Team UUID: {response['team_uuid']}")
        self.cmd2_app.poutput(f"Plan: {response['plan']}")
        self.cmd2_app.poutput("\nMember Info:")
        self.cmd2_app.poutput(table)

    @staticmethod
    def print_bold_red(text):
        print("\033[1;31m" + text + "\033[0m")


class AppShell(Cmd):

    def __init__(self):
        super().__init__()
        del Cmd.do_shell
        del Cmd.do_run_script
        del Cmd.do_edit
        del Cmd.do_py
        del Cmd.do_alias
        del Cmd.do_shortcuts
        del Cmd.do_macro
        del Cmd.do_history
        del Cmd.do_run_pyscript
        self.hidden_commands.append('set')

        self.logged_in = False
        self.output_handler = OutputHandler(self)
        self.request_handler = RequestHandler()
        self.set_window_title("Don't Remember")
        self.prompt = ">> "
        self.current_word = None

    def preloop(self):
        self.output_handler.print_hello()

    login_parser = argparse.ArgumentParser()
    login_parser.add_argument('username', type=str, help='login [username]')

    @with_argparser(login_parser)
    def do_login(self, args):
        """Login as user"""
        if self.logged_in:
            self.output_handler.print_bold_red("Logout first before you login!")
            return
        password = getpass.getpass(prompt='Password: ', stream=None)
        logging.info(f"Login with username: {args.username} and password: {password}")
        # request to login endpoint
        response = self.request_handler.login(args.username, password)

        if response['status'] == 200:
            self.logged_in = True
            self.poutput("Login success")
            # self.fetch_next_word()
        else:
            self.output_handler.print_bold_red(response['message'])

    logout_parser = argparse.ArgumentParser()

    @with_argparser(logout_parser)
    def do_logout(self, args):
        """
        Logout
        :param args:
        :return:
        """
        # check if logged in
        if not self.logged_in:
            self.poutput("Not logged in")
            return
        # request to logout endpoint
        self.request_handler = RequestHandler()
        self.logged_in = False
        self.poutput("Logout success")
        self.output_handler.print_hello()

    signup_parser = argparse.ArgumentParser()
    signup_parser.add_argument('username', type=str, help='signup [username]')

    @with_argparser(signup_parser)
    def do_signup(self, args):
        """Sign up as new user"""
        if self.logged_in:
            self.poutput("Already logged in, please logout first")
            return
        username = args.username
        password = getpass.getpass(prompt='Password: ', stream=None)
        logging.info(f"Signup with username: {username} and password: {password}")
        # request to signup endpoint
        response = self.request_handler.signup(username, password)

        if response['status'] == 200:
            self.poutput("Signup success, Please login to continue")
        else:
            self.poutput("Signup failed, please try again...")
            self.output_handler.print_bold_red(response['message'])

    add_parser = argparse.ArgumentParser()
    add_parser.add_argument('add', type=str, help='Add a word.')

    @with_argparser(add_parser)
    def do_add(self, arg):
        """
        Add a new word.
        :param arg:
        :return:
        """
        if not self.logged_in:
            self.output_handler.print_bold_red("Not logged in")
            return

        word = arg.add
        response = self.request_handler.add_new_word(word)
        if response['status'] == 200:
            self.poutput("Add word success.")
            # self.fetch_next_word()
        else:
            self.output_handler.print_bold_red(response['message'])

    changeteamplan_parser = argparse.ArgumentParser()
    changeteamplan_parser.add_argument('team_uuid', type=str, help='Team uuid')
    changeteamplan_parser.add_argument('new_plan', type=int, help='New plan')

    @with_argparser(changeteamplan_parser)
    def do_changeteamplan(self, arg):
        """
        Set team plan, and the plan is an integer
        """
        if not self.logged_in:
            print("You need to be logged in to access settings")
            return
        # fetch the plan from arg
        team_uuid = arg.team_uuid
        plan = arg.new_plan
        response = self.request_handler.update_team(team_uuid, plan)
        if response['status'] == 200:
            self.poutput("Set plan success")
            # self.fetch_next_word()
        else:
            self.poutput("Set plan failed, please try again...")
            self.output_handler.print_bold_red(response['message'])

    changeplan_parser = argparse.ArgumentParser()
    changeplan_parser.add_argument('new_plan', type=int, help='New Plan')

    @with_argparser(changeplan_parser)
    def do_changeplan(self, arg):
        """
        Set personal plan, and the plan is an integer
        """
        if not self.logged_in:
            print("You need to be logged in to access settings")
            return
        # fetch the plan from arg
        plan = arg.new_plan
        response = self.request_handler.change_plan(plan)
        if response['status'] == 200:
            self.poutput("Set plan success")
            # self.fetch_next_word()
        else:
            self.poutput("Set plan failed, please try again...")
            self.output_handler.print_bold_red(response['message'])

    teaminfo_parser = argparse.ArgumentParser()

    @with_argparser(teaminfo_parser)
    def do_teaminfo(self, arg):
        """
        Check team information.
        :param arg:
        :return:
        """
        if not self.logged_in:
            print("You need to be logged in to access settings")
            return
        # fetch the plan from arg
        response = self.request_handler.team_info()
        if response['status'] == 200:
            self.output_handler.print_teaminfo(response)

        else:
            self.poutput("Check team Information failed, are you in team?")
            self.output_handler.print_bold_red(response['message'])


    learninghistory_parser = argparse.ArgumentParser()

    @with_argparser(learninghistory_parser)
    def do_learninghistory(self, arg):
        """
        Display Learning History.
        :param arg:
        :return:
        """
        if not self.logged_in:
            print("You need to be logged in to access settings")
            return
        # fetch the plan from arg
        response = self.request_handler.word_history()
        if response['status'] == 200:
            self.output_handler.print_learning_history(response)


        else:
            self.poutput("Check learning history failed")
            self.output_handler.print_bold_red(response['message'])

    addteam_parser = argparse.ArgumentParser()
    addteam_parser.add_argument('team_uuid', type=str, help='addteam [team_uuid]')

    @with_argparser(addteam_parser)
    def do_addteam(self, arg):
        """
        Add me to a existing team.
        :param arg:
        :return:
        """
        if not self.logged_in:
            print("You need to be logged in to access settings")
            return
        # fetch the plan from arg
        team_uuid = arg.team_uuid
        response = self.request_handler.add_me_to_team(team_uuid)
        if response['status'] == 200:
            self.poutput("Add team success")
        else:
            self.poutput("Add team failed")
            self.output_handler.print_bold_red(response['message'])


    personalprogress = argparse.ArgumentParser()

    @with_argparser(personalprogress)
    def do_personalprogress(self, arg):
        """
        Check personal progress.
        :param arg:
        :return:
        """
        if not self.logged_in:
            print("You need to be logged in to access settings")
            return
        # fetch the plan from arg
        response = self.request_handler.personal_progress()
        if response['status'] == 200:
            self.poutput(f"--> You have learned \033[31m\033[1m{response['studied_today']}/{response['plan']}\033[0m, today.")

        else:
            self.poutput("Check current progress failed")
            self.output_handler.print_bold_red(response['message'])

    deleteword_parser = argparse.ArgumentParser()
    deleteword_parser.add_argument('word', type=str, help='Delete word.')

    @with_argparser(deleteword_parser)
    def do_deleteword(self, arg):
        """
        Delete a word.
        :param arg:
        :return:
        """
        if not self.logged_in:
            print("You need to be logged in to access settings")
            return
        # fetch the plan from arg
        word = arg.word
        response = self.request_handler.delete_word(word)
        if response['status'] == 200:

            self.poutput("Delete word success")
        else:
            self.poutput("Delete word failed")
            self.output_handler.print_bold_red(response['message'])

    newteam_parser = argparse.ArgumentParser()
    newteam_parser.add_argument('team_name', type=str, help='newteam [team_name]')

    @with_argparser(newteam_parser)
    def do_newteam(self, arg):
        """
        Create a new team.
        :param arg:
        :return:
        """
        if not self.logged_in:
            print("You need to be logged in to access settings")
            return
        # fetch the plan from arg
        team_name = arg.team_name
        response = self.request_handler.new_team(team_name)
        if response['status'] == 200:
            self.poutput("Create new team success")
        else:
            self.poutput("Create new team failed")
            self.output_handler.print_bold_red(response['message'])


    leaveteam_parser = argparse.ArgumentParser()
    leaveteam_parser.add_argument('team_uuid', type=str, help='leaveteam [team_uuid]')

    @with_argparser(leaveteam_parser)
    def do_leaveteam(self, arg):
        """
        leave team
        :param arg:
        :return:
        """
        if not self.logged_in:
            print("You need to be logged in to access settings")
            return
        # fetch the plan from arg
        team_uuid = arg.team_uuid
        response = self.request_handler.leave_team(team_uuid)
        if response['status'] == 200:
            self.poutput("Leave team success")
        else:
            self.poutput("Leave team failed")
            self.output_handler.print_bold_red(response['message'])


    nextword_parser = argparse.ArgumentParser()

    @with_argparser(nextword_parser)
    def do_nextword(self, arg):
        """
        leave team
        :param arg:
        :return:
        """
        if not self.logged_in:
            self.output_handler.print_bold_red("Not Logged In")
            return
        self.fetch_next_word()

    updateword_parser = argparse.ArgumentParser()
    updateword_parser.add_argument('result', type=str, help='update_word [remember | forget]')

    @with_argparser(updateword_parser)
    def do_updateword(self, res):
        """
        update word
        :return:
        """
        response = self.request_handler.update_word(self.current_word, res.result, )
        if response['status'] == 200:
            self.poutput("Update word success")
        else:
            self.poutput("Update word failed")
            self.output_handler.print_bold_red(response['message'])

    def fetch_next_word(self):
        """
        fetch next word from endpoint
        :return:
        """
        response = self.request_handler.next_word()
        if response['status'] == 200:
            self.current_word = response['word']
            self.output_handler.print_word(response)
        elif response['status'] == 404:
            self.output_handler.print_bold_red(response['message'])


if __name__ == '__main__':
    app = AppShell()
    app.cmdloop()
