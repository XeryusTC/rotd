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

import sys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from .server_tools import reset_database

class FunctionalTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_host = arg.split('=')[1]
                cls.server_url = 'http://' + cls.server_host
                cls.against_staging = True
                return # Skip setting up a local test server
        super(FunctionalTestCase, cls).setUpClass()
        cls.server_url = cls.live_server_url
        cls.against_staging = False

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super(FunctionalTestCase, cls).tearDownClass()

    def setUp(self):
        if self.against_staging:
            reset_database(self.server_host)
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.close()
