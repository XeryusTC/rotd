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
