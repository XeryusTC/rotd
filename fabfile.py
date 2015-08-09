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

from fabric.api import env, local, prompt, put, settings, sudo, run
from fabric.context_managers import hide, prefix
from fabric.contrib.console import confirm
from fabric.contrib.files import append, exists, sed
from getpass import getpass
import random
import sys

REPO_URL = 'https://github.com/XeryusTC/rotd.git'

def requirements():
    """Install all the software requirements that pip can't manage."""
    sudo('apt-get install nginx git python3 python3-pip \
            postgresql-server-dev-9.4')
    sudo('pip3 install virtualenv')

def provision():
    """Create the config files to run the site on the server."""
    _setup_variables()
    _settings_prompt()
    env.enable = confirm('Enable site (this activates generated config)?')
    _create_folder_structure(env.dest_folder)
    _setup_database()

    # Make sure all files are downloaded and Django is set up
    _get_latest_source(env.source_folder)
    _update_virtualenv(env.dest_folder)

    _deploy_settings_file()
    _build_and_deploy_system_files(env.source_folder)

    # Finish the final steps that rely on the environment being set up
    _update_database(env.source_folder)
    _update_static_files(env.source_folder)

def deploy():
    """Update the source and associated files."""
    _setup_variables()
    _get_latest_source(env.source_folder)
    _update_virtualenv(env.dest_folder)
    _update_static_files(env.source_folder)
    _update_database(env.source_folder)

def update_settings():
    """Change the environment variables that contain the settings."""
    _setup_variables()
    env.enable = True
    _settings_prompt()
    _deploy_settings_file()

def _setup_variables():
    # skip setup if settings are already setup
    try:
        env.dest_folder
        return
    except AttributeError:
        pass

    run('uptime') # make sure that we have a host set
    env.dest_folder = '/var/www/sites/%s' % (env.host,)
    env.source_folder = env.dest_folder + '/source'

def _setup_database_variables():
    env.db_name = prompt('Database name: ', default='rotd')
    env.db_user = prompt('Database user: ', default='rotd')
    env.db_pass = getpass('Database password: ')
    db_pass2 = getpass('Confirm database password: ')
    if env.db_pass != db_pass2:
        print("Database passwords are not the same.")
        sys.exit(1)

def _settings_prompt():
    _setup_database_variables()
    env.email_host = prompt('Email host: ', default='localhost')
    env.email_port = prompt('Email port: ', default='587')
    env.email_user = prompt('Autosender email address: ',
            default='noreply@%s' % env.email_host)
    env.email_pass = getpass('Email password: ')
    email_pass2    = getpass('Confirm email password: ')
    if env.email_pass != email_pass2:
        print("Email passwords are not the same.")
        sys.exit(1)
    env.setup_ssl  = confirm('Enable SSL?', default=False)

def _deploy_settings_file():
    """Create the EnvironmentFile as required by systemd."""
    # Make sure that settings are set, assume we don't want to upload
    # unless explicitly specified otherwise
    try:
        enable = env.enable
    except AttributeError:
        enable = False
    try:
        env.email_host
    except AttributeError:
        _settings_prompt()

    # Update the file locally
    local('cp deploy_tools/envvars envvars')
    local("sed -i'' s/SITENAME/{}/g   envvars".format(env.host))
    local("sed -i'' s/db_name/{}/g    envvars".format(env.db_name))
    local("sed -i'' s/db_user/{}/g    envvars".format(env.db_user))
    local("sed -i'' s/secret/{}/g     envvars".format(_create_key()))
    local("sed -i'' s/email_host/{}/g envvars".format(env.email_host))
    local("sed -i'' s/email_user/{}/g envvars".format(env.email_user))
    local("sed -i'' s/email_port/{}/g envvars".format(env.email_port))
    with hide('running', 'stdout'):
        local("sed -i'' s/db_password/{}/g    envvars".format(env.db_pass))
        local("sed -i'' s/email_password/{}/g envvars".format(env.email_pass))

    if enable:
        put('envvars', '/etc/default/gunicorn-{}'.format(env.host),
                use_sudo=True, mode=0640)
        sudo('chown {user}:www-data /etc/default/gunicorn-{host}'.format(
                user=env.user, host=env.host))
        with settings(warn_only=True):
            sudo('systemctl restart gunicorn-{}.service'.format(env.host))

def _build_and_deploy_system_files(source_folder):
    try:
        enable = env.enable
    except AttributeError:
        enable = False
    # set up systemd to run the gunicorn service
    gunicorn_template = 'gunicorn-systemd.service.template'
    run('cp %s/deploy_tools/%s /tmp/' % (source_folder, gunicorn_template))
    sed('/tmp/%s' % (gunicorn_template,), 'SITENAME', env.host)

    _deploy_settings_file()

    if enable:
        sudo('mv /tmp/%s /etc/systemd/system/gunicorn-%s.service' % (
            gunicorn_template, env.host))
        sudo('systemctl enable gunicorn-%s.service' % (env.host,))
        sudo('systemctl daemon-reload')
        sudo('systemctl restart gunicorn-%s.service' % (env.host,))

    # Set up nginx
    if env.setup_ssl:
        run('cp %s/deploy_tools/nginx-ssl.conf.template \
                /tmp/nginx.conf.template' % (source_folder,))
    else:
        run('cp %s/deploy_tools/nginx.conf.template /tmp/' % (source_folder,))
    sed('/tmp/nginx.conf.template', 'SITENAME', env.host)
    if enable:
        sudo('mv /tmp/nginx.conf.template /etc/nginx/sites-available/%s' % (
            env.host,))
        sudo('ln -s /etc/nginx/sites-available/%s /etc/nginx/sites-enabled/%s'
            % (env.host, env.host))
        sudo('systemctl restart nginx')

def _create_key(length=50):
    chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYIOPASDFGHJKLZXCVBNM' + \
            '1234567890!@#$%^&*()_+-='
    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

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

def _update_virtualenv(folder):
    virtualenv_folder = folder + '/virtualenv'
    if not exists(virtualenv_folder + '/bin/python'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements/prod.txt' % (virtualenv_folder,
        folder + '/source'))

def _update_static_files(source_folder):
    with prefix('export $(cat /etc/default/gunicorn-{host}|xargs)'.format(
        host=env.host)):
        run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic \
                --noinput' % (source_folder,))

def _setup_database():
    # Test database if user exists, if not then create it
    db_setup = sudo("psql -tAc \"SELECT 1 FROM pg_roles WHERE rolname='%s'\""\
            % (env.db_user,), user='postgres') == '1'
    if not db_setup:
        sudo("psql -c \"CREATE USER %s WITH PASSWORD '%s'\"" % (env.db_user,
            env.db_pass), user='postgres')

    # Test if database is set up, if not create it and give user access
    db_exists = sudo('psql -lqt | cut -d \| -f 1 | grep -w %s | wc -l' %
            (env.db_name,), user='postgres') == '1'
    if not db_exists:
        sudo('psql -c "CREATE DATABASE %s"' % (env.db_name,), user='postgres')
        sudo('psql -c "GRANT ALL PRIVILEGES ON DATABASE %s TO %s"' % (
            env.db_name, env.db_user), user='postgres')


def _update_database(source_folder):
    with prefix('export $(cat /etc/default/gunicorn-{host}|xargs)'.format(
        host=env.host)):
        run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (
            source_folder,))
