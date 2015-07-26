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

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db.utils import IntegrityError

from recipes.models import Recipe
from recipes import factories

class RecipeModelTests(TestCase):
    def test_recipe_has_name_and_description(self):
        Recipe.objects.create(name='Test recipe',
                description='Recipe description')

    def test_recipe_name_required(self):
        r = factories.RecipeFactory(name='')
        with self.assertRaises(ValidationError):
            r.full_clean()

    def test_recipe_description_required(self):
        r = factories.RecipeFactory(description='')
        with self.assertRaises(ValidationError):
            r.full_clean()

    def test_recipe_name_is_unique(self):
        r1 = factories.RecipeFactory(name='Test recipe')
        r1.save()
        with self.assertRaises(IntegrityError):
            r2 = factories.RecipeFactory(name='Test recipe')

    def test_string_representation(self):
        recipe = factories.RecipeFactory(name='test recipe')
        self.assertEquals(str(recipe), 'test recipe')
