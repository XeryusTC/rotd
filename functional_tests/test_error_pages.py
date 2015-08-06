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

from .base import FunctionalTestCase

class ErrorPagesTests(FunctionalTestCase):
    def test_403_page_setup(self):
        # Alice is a visitor who encounters a page she isn't supposed to
        # visit
        self.browser.get(self.server_url + '/403/')
        # She sees a 403 error in the browser's title
        self.assertIn('403', self.browser.title)

        # She also sees a 403 error on the page, along with a text message
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('403', body.text)
        self.assertIn('toegang', body.text.lower())
        self.assertIn('verboden', body.text.lower())

    def test_404_page_setup(self):
        # Alice is a visitor who encounters a non-existing page
        self.browser.get(self.server_url + '/404/')
        # She sees a 404 error in the browser's title
        self.assertIn('404', self.browser.title)

        # She also sees a 404 error on the page, along with some text
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('404', body.text)
        self.assertIn('niet gevonden', body.text.lower())

    def test_500_page_setup(self):
        # Alice visits a page which broke the server for some reason
        self.browser.get(self.server_url + '/500/')
        # She sees a 500 error in the browser's title
        self.assertIn('500', self.browser.title)

        # She also sees a 500 error on the page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('500', body.text)
