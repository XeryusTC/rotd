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

from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTestCase

class ContactPageTests(FunctionalTestCase):

    def test_navbar(self):
        # Alice is a visitor who sees a navbar on the page with two links
        self.browser.get(self.server_url)
        navbar = self.browser.find_element_by_tag_name('nav')

        # There are two links in the navbar, one for the homepage and one
        # for the contact page, Alice decides to click the contact page
        # link. There is also a brand in the navbar
        brand = navbar.find_element_by_class_name('navbar-brand')
        self.assertEqual('Recept van de dag', brand.text)
        navbar.find_element_by_link_text('Contact').click()
        # On the page is a header with a contact form
        header = self.browser.find_element_by_tag_name('h1')
        self.assertEquals('Contact', header.text)
        form = self.browser.find_element_by_tag_name('form')

        # Alice decides to go back to the homepage where she will find the
        # recipe of the day
        self.browser.find_element_by_link_text('Recept van de dag').click()
        header = self.browser.find_element_by_tag_name('h1')
        self.assertEquals('Recept van de dag', header.text)

    def test_contact_form(self):
        # Alice is a visitor who goes to the contact page
        self.browser.get(self.server_url + '/contact/')

        # She finds a form there and decides to write a message
        name = self.browser.find_element_by_name('name')
        email = self.browser.find_element_by_name('email')
        subject = self.browser.find_element_by_name('subject')
        body = self.browser.find_element_by_css_selector("textarea[name='body']")
        submit = self.browser.find_element_by_tag_name('button')

        name.send_keys('Test Client')
        email.send_keys('text@example.com')
        subject.send_keys('Nice website!')
        body.send_keys('Nice website!')
        submit.click()

        # After submitting she should be redirected to a page that
        # thanks her for her feedback
        location = self.browser.current_url
        self.assertTrue(location.endswith('/contact/thanks/'))
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Bedankt voor je bericht', body.text)
