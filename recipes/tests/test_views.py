from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from recipes.views import home_page
from recipes.models import Recipe

class HomePageViewTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_inherits_from_base_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'rotd/base.html')

    def test_home_page_uses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'recipes/home.html')

    def test_home_page_has_recipe(self):
        Recipe.objects.create(name='test')
        response = self.client.get('/')
        self.assertIsInstance(response.context['recipe'], Recipe)

    def test_home_page_shows_any_recipe_name(self):
        Recipe.objects.create(name='test recipe')
        request = HttpRequest()
        response = home_page(request).content.decode()

        self.assertTrue(any([(recipe.name in response)
            for recipe in Recipe.objects.all()]))
