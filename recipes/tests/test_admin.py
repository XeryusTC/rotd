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

from django.test import TestCase

from recipes.admin import RecipeAdmin
from recipes.models import Recipe
from rotd.admin import admin_site

class RecipeAdminTest(TestCase):
    def test_recipe_admin_creates_slug_automatically(self):
        """This is just a smoke test, the FT is more reliable"""
        admin = RecipeAdmin(Recipe, admin_site)
        admin.prepopulated_fields['slug']
