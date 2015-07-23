from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import factory

from .base import FunctionalTestCase

class DjangoAdminUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'admin%d' % n)
    email = factory.LazyAttribute(lambda o: '%s@xeryus.nl' % o.username)
    password = factory.PostGenerationMethodCall('set_password', 'admin')

    is_superuser = True
    is_staff = True
    is_active = True

class DjangoAdminTests(FunctionalTestCase):
    def test_can_create_recipe_via_admin_site(self):
        # Set up admin accounts
        admin = DjangoAdminUserFactory()
        # Alice is an admin that wants to visit the admin page
        self.browser.get(self.server_url + '/admin/')

        # She sees the administration heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('ROTD administration', body.text)

        # She types in her username and password and tries to log in
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(admin.username)
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

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
