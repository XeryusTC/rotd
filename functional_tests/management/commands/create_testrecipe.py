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

import datetime
from django.core.management.base import BaseCommand
from recipes.models import Recipe

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('name', nargs='+')

    def handle(self, *args, **options):
        r = Recipe(name=' '.join(options['name']), description='description')
        r.save()
        r.add_date = datetime.date.today() - datetime.timedelta(days=2)
        r.save()
        self.stdout.write(r.slug)
