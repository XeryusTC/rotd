from os import path
import subprocess

THIS_FOLDER = path.dirname(path.abspath(__file__))

def create_admin_on_server(host, username, password, email):
    return subprocess.check_call([
        'fab',
        'create_admin_on_server:username={},password={},email={}'.format(
            username, password, email),
        '--host={}'.format(host),
        '--hide=everything,status',
        ], cwd=THIS_FOLDER)

def reset_database(host):
    subprocess.check_call(['fab', 'reset_database', '--host={}'.format(host)],
            cwd=THIS_FOLDER)

def create_testrecipe_on_server(host):
    subprocess.check_call(
            ['fab', 'create_testrecipe_on_server', '--host={}'.format(host)],
            cwd=THIS_FOLDER)
