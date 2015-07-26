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
