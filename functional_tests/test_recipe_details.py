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

from random import randint

from .base import FunctionalTestCase
from .server_tools import create_testrecipe_on_server, create_ingredient, \
    add_ingredient_to_recipe
import recipes.factories

class RecipeDetailPageTest(FunctionalTestCase):
    def test_detail_page_exists(self):
        # Create a dummy recipe
        if self.against_staging:
            recipe = create_testrecipe_on_server(self.server_host,
                    'Test recipe')

            ingreds = ['Ingredient %s' % i for i in range(3)]
            for i in ingreds:
                id = create_ingredient(self.server_host, i)
                add_ingredient_to_recipe(self.server_host, id, recipe)
        else:
            recipe = recipes.factories.RecipeFactory(name='Test recipe')
            ingreds = recipes.factories.IngredientFactory.create_batch(3)
            usage = [recipes.factories.IngredientUsageFactory(recipe=recipe,
                ingredient=i, quantity=randint(1, 10)) for i in ingreds]
            recipe = recipe.slug
            ingreds = [ str(i) for i in usage ]

        # Alice is a visitor who remembered the specific url for a recipe
        self.browser.get(self.server_url + '/recept/' + recipe + '/')

        # The title of the page contains the name of the recipe
        self.assertEqual(self.browser.title, 'Test recipe')

        # The main header says it is the recipe detail page
        header = self.browser.find_element_by_tag_name('h1')
        self.assertEqual(header.text, 'Recept informatie')

        # There is a header which just says the name of the recipe
        header = self.browser.find_element_by_id('recipe')
        self.assertEqual(header.text, 'Test recipe')

        # The description of the recipe is also on the page
        desc = self.browser.find_element_by_id('description')
        self.assertGreater(len(desc.text), 0)

        # There is also a list of ingredients on the page
        ingredient_list = self.browser.find_element_by_id('ingredients')
        ingredients = ingredient_list.find_elements_by_tag_name('li')
        self.assertEqual(len(ingredients), 3)
        # The list contains the right ingredients, each one starts with a
        # number
        for i in ingredients:
            int(i.text[0])
            self.assertIn(i.text, ingreds)
