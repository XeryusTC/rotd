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

from django.test import LiveServerTestCase
from selenium import webdriver

from .base import FunctionalTestCase
from .server_tools import create_testrecipe_on_server
import recipes.factories

class HomePageRecipeTests(FunctionalTestCase):
    def test_can_see_todays_recipe(self):
        # Create a dummy recipe
        if self.against_staging:
            create_testrecipe_on_server(self.server_host)
        else:
            recipes.factories.RecipeFactory()

        # Alice goes to our website
        self.browser.get(self.server_url)

        # She notices that the title says 'Recept van de dag'
        self.assertIn('Recept van de dag', self.browser.title)

        # There is also a header on the page that says 'Recept van de dag'
        header_text = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Recept van de dag', header_text.text)

        # There is a title of a recipe on the page
        title = self.browser.find_element_by_id('recipe')
        self.assertGreater(len(title.text), 0)
        # There is also some description
        desc = self.browser.find_element_by_id('description')
        self.assertGreater(len(desc.text), 0)

if __name__ == "__main__":
    unittest.main()
