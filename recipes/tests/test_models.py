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
from django.db import models
from django.db.utils import IntegrityError

from recipes.models import Recipe, Ingredient
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

    def test_recipe_slug_doesnt_change_when_updating_name(self):
        r = factories.RecipeFactory()
        slug = r.slug

        r.name = 'new name'
        r.save()

        self.assertEqual(slug, r.slug)

    def test_recipe_has_slug(self):
        r = factories.RecipeFactory()
        self.assertGreater(len(r.slug), 0)

    def test_recipe_slugs_are_unique(self):
        rs = factories.RecipeFactory.create_batch(size=2)
        self.assertNotEqual(rs[0].slug, rs[1].slug)

    def test_recipe_slugs_are_valid_slugs(self):
        r = factories.RecipeFactory(name='Th!s is 4 WeIrD sl_g nam#()?')
        # We do not care about "weird" slugs starting with a dash or other
        # malformed slugs
        self.assertRegex(r.slug, r'^[a-z0-9_-]+$')

    def test_recipe_specifies_absolute_url(self):
        r = factories.RecipeFactory()
        self.assertIsInstance(r.get_absolute_url(), str)
        self.assertGreater(len(r.get_absolute_url()), 0)


class IngredientModelTests(TestCase):
    def test_ingredient_has_name(self):
        Ingredient.objects.create(name='Test recipe')

    def test_ingredient_name_required(self):
        i = factories.IngredientFactory(name='')
        with self.assertRaises(ValidationError):
            i.full_clean()

    def test_ingredient_can_be_used_in_recipe(self):
        il = factories.IngredientFactory.create_batch(5)
        r = factories.RecipeFactory()
        r.ingredient_set.add(*il)
        for i in il:
            self.assertIn(r, i.used_in.all())
