from simplegithub.SimpleGithub import SimpleGithub

if __name__ == '__main__':
    sg = SimpleGithub()

    sg.get_user_repos()
    sg.choose_a_repo()
    sg.clone_chosen_repo()
