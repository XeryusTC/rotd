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

from os import path
import subprocess

THIS_FOLDER = path.dirname(path.abspath(__file__))

def create_admin_on_server(host, username, password, email):
    return subprocess.check_call(['fab',
        'create_admin_on_server:username={},password={},email={}'.format(
            username, password, email), '--host={}'.format(host)],
        cwd=THIS_FOLDER)

def reset_database(host):
    subprocess.check_call(['fab', 'reset_database', '--host={}'.format(host)],
            cwd=THIS_FOLDER)

def create_testrecipe_on_server(host, name):
    return subprocess.check_output(['fab',
        'create_testrecipe_on_server:name={}'.format(name),
        '--host={}'.format(host), '--hide=everything,status'],
        cwd=THIS_FOLDER).decode().strip()
