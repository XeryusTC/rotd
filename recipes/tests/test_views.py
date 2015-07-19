from datetime import date, timedelta
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from recipes.models import Recipe
from recipes.views import home_page, todays_recipe
from recipes import factories

class HomePageViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(HomePageViewTest, cls).setUpClass()
        factories.RecipeFactory()

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


class EveryDayNewRecipeTest(TestCase):
    """Tests that each day has a different recipe than the day before
    by induction"""
    @classmethod
    def setUpClass(cls):
        super(EveryDayNewRecipeTest, cls).setUpClass()
        factories.RecipeFactory.create_batch(size=50)

    def test_todays_recipe_returns_recipe(self):
        self.assertIsInstance(todays_recipe(), Recipe)

    def test_todays_recipe_returns_recipe_in_database(self):
        self.assertIn(todays_recipe(), Recipe.objects.all())

    def test_todays_recipe_default_is_today(self):
        self.assertEqual(todays_recipe(), todays_recipe(date.today()))

    def test_new_day_means_new_recipe(self):
        today = date.today()
        tomorrow = today + timedelta(days=1)
        self.assertNotEqual(todays_recipe(today),
                todays_recipe(tomorrow))

    def test_home_page_uses_recipe_selector(self):
        response = self.client.get('/')
        self.assertEqual(todays_recipe(), response.context['recipe'])
