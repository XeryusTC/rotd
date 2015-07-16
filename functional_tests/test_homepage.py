import unittest
from selenium import webdriver

class HomePageRecipeTests(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.close()

    def test_django_working(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Django', self.browser.title)

if __name__ == "__main__":
    unittest.main()
