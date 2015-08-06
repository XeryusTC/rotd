# -*- coding: utf-8 -*-
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

from datetime import date, datetime, timedelta
from django.core import mail
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase, RequestFactory
import unittest
from unittest.mock import Mock, patch

from recipes.forms import ContactForm
from recipes.models import Recipe
from recipes.views import home_page, todays_recipe, ContactView
from recipes import factories

class HomePageViewTest(TestCase):
    def get_homepage_content(self):
        request = HttpRequest()
        return home_page(request)

    def test_root_url_resolves_to_home_page_view(self):
        factories.RecipeFactory()
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_uses_correct_templates(self):
        factories.RecipeFactory()
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'recipes/home.html')

    def test_home_page_degrades_gracefully_when_no_recipe(self):
        response = self.get_homepage_content().content.decode()
        self.assertNotIn('Exception', response)

    def test_home_page_has_recipe(self):
        factories.RecipeFactory()
        response = self.client.get('/')
        self.assertIsInstance(response.context['recipe'], Recipe)

    def test_home_page_shows_any_recipe_name(self):
        factories.RecipeFactory()
        response = self.get_homepage_content().content.decode()

        self.assertTrue(any([(recipe.name in response)
            for recipe in Recipe.objects.all()]))

    def test_recipe_description_newlines_are_converted_to_br(self):
        factories.RecipeFactory(description='line1\nline2')
        response = self.get_homepage_content().content.decode()

        self.assertIn('line1<br />line2', response)


class EveryDayNewRecipeTest(unittest.TestCase):
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
        self.assertNotEqual(todays_recipe(today), todays_recipe(tomorrow))

    @patch('recipes.views.todays_recipe')
    def test_home_page_uses_recipe_selector_new(self, mock_todays_recipe):
        response = home_page(HttpRequest())
        self.assertTrue(mock_todays_recipe.called)

    def test_adding_new_recipe_doesnt_change_todays_recipe(self):
        today = date.today()
        before = todays_recipe(today)
        factories.RecipeFactory(post=True)
        after = todays_recipe(today)
        self.assertEqual(before, after)

    def test_changing_recipe_doesnt_change_todays_recipe(self):
        today = date.today()
        before = todays_recipe(today)
        before.name = 'Changed name'
        before.save()
        after = todays_recipe(today)
        self.assertEqual(before, after)


class ContactPageTest(TestCase):
    def test_contact_page_returns_contact_template(self):
        response = self.client.get('/contact/')
        self.assertTemplateUsed(response, 'recipes/contact.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_contact_thanks_page_uses_correct_templates(self):
        response = self.client.get('/contact/thanks/')
        self.assertTemplateUsed(response, 'recipes/contact_thanks.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_contact_page_holds_contact_form(self):
        response = self.client.get('/contact/')
        self.assertIsInstance(response.context['form'], ContactForm)

    def test_form_sends_mail_on_POST(self):
        request = RequestFactory().post('/contact/',
                data={'name': 'Test Case', 'email': 'test@test.test',
                    'subject': 'Test subject', 'body': 'Test body'})

        contact = ContactView.as_view()
        contact(request)

        self.assertEqual(len(mail.outbox), 1)
