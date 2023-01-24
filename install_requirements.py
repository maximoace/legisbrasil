import os

if __name__ == '__main__':
    path = os.path.dirname(__file__)
    if not os.path.exists('.venv'):
        set_folder = f' cd {path} & '
        set_venv = f'python -m venv .venv & '
        set_update = f'python -m pip install -U pip wheel setuptools'
        activate_venv = f'cmd /c ".venv\Scripts\\activate & {set_update} & '
        install_requirements = f'pip install -r requirements.txt'
        command = f'{set_folder}{set_venv}{activate_venv}{install_requirements}'
        os.system(command)