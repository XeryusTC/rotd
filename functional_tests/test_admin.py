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

from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import LiveServerTestCase
from django.core.management import call_command
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip

import factory

from .base import FunctionalTestCase
from .server_tools import create_admin_on_server, create_testrecipe_on_server
import recipes.factories

class DjangoAdminTests(FunctionalTestCase):
    def setUp(self):
        super(DjangoAdminTests, self).setUp()

        # Set up admin account
        self.username = 'testadmin'
        self.password = 'testadmin'
        if self.against_staging:
            create_admin_on_server(self.server_host, self.username,
                    self.password, 'a@b.com')
        else:
            call_command('create_admin', self.username, self.password,
                    'a@b.com')

    def admin_login(self, username, password,
            url='/administratievehandelingen/'):
        self.browser.get(self.server_url + url)
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(username)
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

    def test_can_create_recipe_via_admin_site(self):
        # Alice is an admin that wants to visit the admin page
        self.browser.get(self.server_url + '/administratievehandelingen/')

        # She sees the administration heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('ROTD administration', body.text)

        self.admin_login(self.username, self.password)

        # Her username and password are accepted and she is taken to
        # the Site administration page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

        # She sees that she can edit recipes
        recipe_links = self.browser.find_elements_by_link_text('Recipes')
        self.assertEqual(len(recipe_links), 2)
        # She follows the link, sees there are no recipes and adds a recipe
        recipe_links[1].click()
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('0 recipes', body.text)
        self.browser.find_element_by_link_text('Add recipe').click()

        # A form appears and she fills it in
        name_field = self.browser.find_element_by_name('name')
        name_field.send_keys('Test recipe')
        desc_field = self.browser.find_element_by_name('description')
        desc_field.send_keys('This is a test description')
        name_field.send_keys(Keys.RETURN)

        # She sees that there is one recipe on the page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('1 recipe', body.text)

    def test_can_add_ingredients_to_recipe_via_admin_site(self):
        # Create a dummy recipe
        if self.against_staging:
            create_testrecipe_on_server(self.server_host, 'Test recipe')
        else:
            recipes.factories.RecipeFactory(name='Test recipe')
        # Alice is an admin that wants to add an ingredient
        self.admin_login(self.username, self.password)

        # She navigates to the ingredients
        self.browser.find_element_by_link_text('Ingredients').click()

        # There should be no ingredients yet
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('0 ingredients', body.text)
        # She goes to add an ingredient
        self.browser.find_element_by_link_text('Add ingredient').click()

        # A form appears and she completes it
        name_field = self.browser.find_element_by_name('name')
        name_field.send_keys('Test ingredient')
        name_field.send_keys(Keys.RETURN)

        # She now sees that the ingredient is on the list
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('1 ingredient', body.text)
        self.assertIn('Test ingredient', body.text)

        # She goes to the recipes
        self.browser.get(self.server_url + '/administratievehandelingen')
        recipe_links = self.browser.find_elements_by_link_text('Recipes')
        recipe_links[1].click()
        # There should be a recipe, which she clicks
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('1 recipe', body.text)
        results = self.browser.find_element_by_id('result_list')
        link = results.find_elements_by_tag_name('a')[0]
        link.click()

        # There is an area where she can add ingredients, she selects
        # the first box and selects the newly created ingredient
        relation = self.browser.find_element_by_id('Ingredient_used_in-0')
        select = relation.find_element_by_tag_name('select')
        options = select.find_elements_by_tag_name('option')
        self.assertEqual(len(options), 2)
        self.assertIn('Test ingredient', options[1].text)
        options[1].click()

        # She saves the recipe
        submit = self.browser.find_element_by_name('_continue')
        submit.click()

        # She goes to the recipe detail page
        self.browser.find_element_by_link_text('View on site').click()

        # On the recipe detail page the ingredient is listed in the
        # ingredient section
        ingredient_list = self.browser.find_element_by_id('ingredients')
        ingredients = ingredient_list.find_elements_by_tag_name('li')
        self.assertEqual(len(ingredients), 1)
        self.assertEqual('Test ingredient', ingredients[0].text)

    def test_admin_site_links_to_recipe_detail_page(self):
        # Create a dummy recipe
        if self.against_staging:
            create_testrecipe_on_server(self.server_host, 'Test recipe')
        else:
            recipes.factories.RecipeFactory(name='Test recipe')
        # Alice is an admin who goes to the admin site
        self.admin_login(self.username, self.password)

        # She navigates to the recipes
        recipe_links = self.browser.find_elements_by_link_text('Recipes')
        recipe_links[1].click()

        # Sanity check, there should be recipes available
        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('0 recipes', body.text)

        # She clicks on the first recipe in the list
        results = self.browser.find_element_by_id('result_list')
        link = results.find_elements_by_tag_name('a')[0]
        link.click()

        # She sees a 'visit on site' link and clicks it
        link = self.browser.find_element_by_link_text('View on site')
        link.click()

        # She ends up at the detail page of the recipe (smoke test)
        self.wait_for(lambda : self.assertIn('/recept/',
            self.browser.current_url))
        self.assertEqual(self.browser.title, 'Test recipe')

    @skip
    def test_admin_honeypot_set_up(self):
        # Trudy tries to break into the admin site at the default url
        self.browser.get(self.server_url + '/admin/')

        # She sees the administration heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        # She types in a username and password and tries to log in
        self.admin_login('qwerty', 'abcdef', '/admin/')
        # She sees an error message
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Please enter the correct username and pass', body.text)

        # Alice is a valid admin who can login at the right URL
        self.admin_login(self.username, self.password)

        # She goes to the list of login attempts
        attempts = self.browser.find_element_by_link_text('Login attempts')
        attempts.click()

        # She selects the login attempts for today and sees the login attempt
        self.browser.find_element_by_link_text('Today').click()
        results = self.browser.find_element_by_id('result_list')
        self.assertIn('qwerty', results.text)
