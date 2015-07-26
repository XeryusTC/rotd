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

from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('username')
        parser.add_argument('password')
        parser.add_argument('email')

    def handle(self, *args, **options):
        call_command('createsuperuser', username=options['username'],
                email=options['email'], interactive=False)
        u = User.objects.get(username=options['username'])
        u.set_password(options['password'])
        u.save()
