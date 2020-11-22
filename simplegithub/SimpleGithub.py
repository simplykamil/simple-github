import getpass
import sys

import requests
from cryptography.fernet import Fernet

from simplegithub.Repo import Repo


class SimpleGithub:
    def __init__(self):
        """
        Create instance of simple github, load credentials
        """

        self.creds_file = '.simple-github.creds'
        self.key_file = '.simple-github.key'
        self.key = None
        self.username = None
        self.password = None
        self.token = None
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        self.repos = list()
        self.chosen_repo = None
        self.should_quit = False

        self.load_credentials()

    def load_credentials(self):
        """
        Load credentials either from file or user input and save
        :rtype: None
        """

        try:
            with open(self.creds_file, 'r') as credfile, open(self.key_file, 'rb') as keyfile:
                creds = credfile.read()
                credfile.close()

                self.key = keyfile.read()
                keyfile.close()

                f = Fernet(self.key)

                print()
                self.username, self.password, self.token = creds.split(' ')
                print('Credentials loaded')

        except:
            print()
            print('Credentials file not detected')
            username = input('Please enter your github username: ')
            password = getpass.getpass(prompt=f'Please enter password for user {username}: ')
            token = getpass.getpass(prompt=f'Please enter token for user {username}: ')

            self.key = Fernet.generate_key()
            f = Fernet(self.key)

            creds = f'{username} {password} {token}'.encode()
            self.username, self.password, self.token = creds.decode().split(' ')

            self.save_credentials(creds)

    def save_credentials(self, creds: bytes):
        """
        Save credentials
        :param creds: credentials
        :rtype: None
        """

        try:
            with open(self.creds_file, 'wb') as credfile, open(self.key_file, 'wb') as keyfile:
                credfile.write(creds)
                credfile.close()

                keyfile.write(self.key)
                keyfile.close()

                print()
                print('Credentials saved')
        except Exception as e:
            print(e)

    def get_user_repos(self):
        """
        Get user repos
        :return: user repos
        :rtype: list
        """

        req = requests.get('https://api.github.com/user/repos', headers=self.headers, auth=(self.username, self.token))
        status_code = req.status_code

        if status_code == 200:
            json = req.json()
            for repo in json:
                # id, clone_url, name
                repo_id = repo.get('id')
                clone_url = repo.get('clone_url')
                name = repo.get('name')

                self.repos.append(Repo(repo_id, name, clone_url))

            return self.repos
        else:
            # TODO: // PANIC MODE
            print(status_code)

    def choose_a_repo(self):
        """
        Prompt the user to chose a repo
        :rtype: None
        """

        print()

        for i, repo in enumerate(self.repos):
            print(f'{i + 1} - {repo}')

        print()

        while not self.chosen_repo and not isinstance(self.chosen_repo, int):
            inp = input('Please chose a repo or Q to quit: ')

            try:
                if inp in ['Q', 'q']:
                    self.should_quit = True
                    break
                elif not inp.isdigit() or int(inp) not in range(1, len(self.repos) + 1):
                    print('You need to choose a repo')
                else:
                    self.chosen_repo = i
                    print()
                    print(f'Chosen repo {self.repos[i]}')
            except:
                pass

        if self.should_quit:
            print('See ya')
            sys.exit(1)

    def clone_chosen_repo(self):
        """
        Clone chosen repo
        :rtype: None
        """

        print(f'Cloning {self.repos[self.chosen_repo]}')
        self.repos[self.chosen_repo].clone(self.username, self.password)

        print()
