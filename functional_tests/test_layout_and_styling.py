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
