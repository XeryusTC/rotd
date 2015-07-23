from fabric.api import env, run

def _get_base_folder(host):
    return '/var/www/sites/' + host

def _get_manage_py(host):
    return '{path}/virtualenv/bin/python {path}/source/manage.py'.format(
            path=_get_base_folder(host))

def reset_database():
    run('{manage} flush --noinput'.format(manage=_get_manage_py(env.host)))

def create_admin_on_server(username, password, email):
    run('{manage} create_admin {username} {password} {email}'.format(
        manage=_get_manage_py(env.host), username=username, password=password,
        email=email))

def create_testrecipe_on_server():
    run('{manage} create_testrecipe'.format(manage=_get_manage_py(env.host)))
