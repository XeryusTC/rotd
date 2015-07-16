from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from recipes.views import home_page

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_uses_correct_template(self):
        request = HttpRequest()
        response = home_page(request)
        expected = render_to_string('recipes/home.html')
        self.assertEqual(response.content.decode(), expected)
