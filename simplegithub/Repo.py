import subprocess


class Repo:
    """
    Repository object
    """

    def __init__(self, id, name, clone_url):
        self.id = id
        self.name = name
        self.clone_url = clone_url

    def __repr__(self):
        """
        Representation
        :return: a representation of the repo
        :rtype: str
        """

        return f'Repo {self.name} | id: {self.id}'

    def clone(self, username, password):
        """
        Clone the repo
        :param username: username
        :type username: str
        :param password: password
        :type password: str
        :rtype: None
        """

        clone_url = self.clone_url.replace('https://github.com', f'https://{username}:{password}@github.com')

        res = subprocess.call(
            ['git', 'clone', clone_url])
