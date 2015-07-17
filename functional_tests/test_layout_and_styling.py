from django.test import LiveServerTestCase
from selenium import webdriver
import selenium.common.exceptions

import recipes.factories

class LayoutTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.close()

    def test_bootstrap_files_are_loaded(self):
        # Load some default data
        recipes.factories.RecipeFactory()

        # Alice goes to the homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # When looking at the source she notices that bootstrap css is loaded
        links = self.browser.find_elements_by_tag_name('link')
        self.assertTrue(any([ 'bootstrap' in link.get_attribute('href')
            for link in links ]))

        # There is also a bootstrap javascript file loaded at the end
        scripts = self.browser.find_elements_by_tag_name('script')
        self.assertTrue(any([ 'bootstrap' in script.get_attribute('src')
            for script in scripts ]))
