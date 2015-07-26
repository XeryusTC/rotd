# -*- coding: utf-8 -*-
# ROTD suggest a recipe to cook for dinner, changing the recipe every day.
# Copyright © 2015 Xeryus Stokkel

# ROTD is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.

# ROTD is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
# License for more details.

# You should have received a copy of the GNU General Public License
# along with ROTD.  If not, see <http://www.gnu.org/licenses/>.

from fabric.api import env, local, prompt, settings, sudo, run
from fabric.contrib.console import confirm
from fabric.contrib.files import append, exists, sed
from getpass import getpass
import random

REPO_URL = 'https://github.com/XeryusTC/rotd.git'

dest_folder = None
source_folder = None
db_name = None
db_user = None
db_pass = None

def provision():
    sudo('apt-get install nginx git python3 python3-pip \
            postgresql-server-dev-9.4')
    sudo('pip3 install virtualenv')
    _setup_variables(True)
    _setup_database()

    # Make sure all files are downloaded and Django is set up
    deploy()

    _build_and_deploy_system_files(source_folder)

def deploy():
    _setup_variables()
    _create_folder_structure(dest_folder)
    _get_latest_source(source_folder)
    _update_virtualenv(dest_folder)
    _update_settings(source_folder, env.host)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _setup_variables(database=False):
    global dest_folder, source_folder
    if dest_folder != None:
        return
    run('uptime') # make sure that we have a host set
    dest_folder = '/var/www/sites/%s' % (env.host,)
    source_folder = dest_folder + '/source'
    if database:
        _setup_database_variables()

def _setup_database_variables():
    global db_name, db_user, db_pass
    db_name = prompt('Database name: ', default='rotd')
    db_user = prompt('Database user: ', default='rotd')
    db_pass = getpass('Database password: ')

def _build_and_deploy_system_files(source_folder):
    enable = confirm('Enable site?')
    # set up systemd to run the gunicorn service
    gunicorn_template = 'gunicorn-systemd.service.template'
    run('cp %s/deploy_tools/%s /tmp/' % (source_folder, gunicorn_template))
    sed('/tmp/%s' % (gunicorn_template,), 'SITENAME', env.host)
    if enable:
        sudo('mv /tmp/%s /etc/systemd/system/gunicorn-%s.service' % (
            gunicorn_template, env.host))
        sudo('systemctl enable gunicorn-%s.service' % (env.host,))
        sudo('systemctl daemon-reload')
        sudo('systemctl restart gunicorn-%s.service' % (env.host,))

    # Set up nginx
    run('cp %s/deploy_tools/nginx.conf.template /tmp/' % (source_folder,))
    sed('/tmp/nginx.conf.template', 'SITENAME', env.host)
    if enable:
        sudo('mv /tmp/nginx.conf.template /etc/nginx/sites-available/%s' % (
            env.host,))
        sudo('systemctl restart nginx')


def _create_folder_structure(folder):
    for subfolder in ('static', 'virtualenv', 'source'):
        sudo('mkdir -p %s/%s' % (folder, subfolder))
        sudo('chown -R %s:www-data %s' % (env.user, folder,))

def _get_latest_source(source_folder):
    if exists('%s/.git' % (source_folder,)):
        run('cd %s && git fetch' % (source_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))

def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/rotd/settings.py'
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(settings_path, 'DOMAIN = "localhost"', 'DOMAIN = "%s"' % site_name)

    # Set up secret key
    secret_key_file = source_folder + '/rotd/secret_key.py'
    if not exists(secret_key_file):
        chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYIOPASDFGHJKLZXCVBNM' + \
                '1234567890!@#$%^&*()_+-='
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, 'SECRET_KEY = "%s"' % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

    # Set up database
    database_file = source_folder + '/rotd/database.py'
    if not exists(database_file):
        if db_name is None:
            _setup_database_variables()

        run('cd %s && cp deploy_tools/database.py %s' % (source_folder,
            database_file))
        sed(database_file, '"NAME": ""', '"NAME": "%s"' % (db_name,))
        sed(database_file, '"USER": ""', '"USER": "%s"' % (db_user,))
        sed(database_file, '"PASSWORD": ""',
            '"PASSWORD": "%s"' % (db_pass,))
    append(settings_path, '\nfrom .database import DATABASES')

def _update_virtualenv(folder):
    virtualenv_folder = folder + '/virtualenv'
    if not exists(virtualenv_folder + '/bin/python'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (virtualenv_folder,
        folder + '/source'))

def _update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic \
            --noinput' % (source_folder,))

def _setup_database():
    # Test database if user exists, if not then create it
    db_setup = sudo("psql -tAc \"SELECT 1 FROM pg_roles WHERE rolname='%s'\"" \
            % (db_user,), user='postgres') == '1'
    if not db_setup:
        sudo("psql -c \"CREATE USER %s WITH PASSWORD '%s'\"" % (db_user, db_pass),
                user='postgres')

    # Test if database is set up, if not create it and give user access
    db_exists = sudo('psql -lqt | cut -d \| -f 1 | grep -w %s | wc -l' %
            (db_name,), user='postgres') == '1'
    if not db_exists:
        sudo('psql -c "CREATE DATABASE %s"' % (db_name,), user='postgres')
        sudo('psql -c "GRANT ALL PRIVILEGES ON DATABASE %s TO %s"' % (db_name,
            db_user), user='postgres')


def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (
        source_folder,))
