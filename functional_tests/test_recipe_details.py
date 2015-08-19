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

from .base import FunctionalTestCase
from .server_tools import create_testrecipe_on_server
import recipes.factories

class RecipeDetailPageTest(FunctionalTestCase):
    def test_detail_page_exists(self):
        # Create a dummy recipe
        if self.against_staging:
            recipe = create_testrecipe_on_server(self.server_host)
        else:
            recipe = recipes.factories.RecipeFactory()
            recipe = recipe.slug

        # Alice is a visitor who remembered the specific url for a recipe
        self.browser.get(self.server_url + '/recipe/' + recipe + '/')

        # The title of the page contains the name of the recipe
        self.assertGreater(len(self.browser.title), 0)
        self.assertNotIn('Recept van de dag', self.browser.title)

        # There is a header which just says the name of the recipe
        header = self.browser.find_element_by_tag_name('h1')
        self.assertGreater(len(header.text), 0)

        # The description of the recipe is also on the page
        desc = self.browser.find_element_by_id('description')
        self.assertGreater(len(desc.text), 0)

        # There is also a list of ingredients on the page
        ingredient_list = self.browser.find_element_by_id('ingredients')
        ingredients = ingredient_list.find_elements_by_tag_name('li')
        self.assertGreater(len(ingredients), 0)
