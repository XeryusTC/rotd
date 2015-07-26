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
import selenium.common.exceptions

from .base import FunctionalTestCase
import recipes.factories

class LayoutTest(FunctionalTestCase):
    def test_bootstrap_files_are_loaded(self):
        # Load some default data
        recipes.factories.RecipeFactory()

        # Alice goes to the homepage
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # When looking at the source she notices that bootstrap css is loaded
        links = self.browser.find_elements_by_tag_name('link')
        self.assertTrue(any([ 'bootstrap' in link.get_attribute('href')
            for link in links ]))

        # There is also a bootstrap javascript file loaded at the end
        scripts = self.browser.find_elements_by_tag_name('script')
        self.assertTrue(any([ 'bootstrap' in script.get_attribute('src')
            for script in scripts ]))

    def test_footer_is_present(self):
        # Alice goes to the homepage
        self.browser.get(self.server_url)

        # At the bottom she sees a bit of text
        footer = self.browser.find_element_by_tag_name('footer')
        self.assertIn('Affero', footer.text)
