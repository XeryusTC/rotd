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
        header_text = self.browser.get_element_by_tag_name('h1')
        self.assertIn('Recept van de dag', header_text.text)

if __name__ == "__main__":
    unittest.main()
