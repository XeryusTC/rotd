import unittest
from selenium import webdriver

class HomePageRecipeTests(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.close()

    def test_can_see_todays_recipe(self):
        # Alice goes to our website
        self.browser.get('http://localhost:8000')

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
