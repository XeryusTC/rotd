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

from django.http import HttpRequest
from unittest import TestCase
from rotd.middleware import RemoteAddrMiddleware

class MiddlewareTests(TestCase):
    def test_proxy_remote_addr_set(self):
        request = HttpRequest()
        request.META['HTTP_X_FORWARDED_FOR'] = '255.255.255.255'
        remote = RemoteAddrMiddleware()

        remote.process_request(request)

        self.assertEqual(request.META['REMOTE_ADDR'], '255.255.255.255')

    def test_dont_change_remote_addr_when_not_proxying(self):
        request = HttpRequest()
        remote = RemoteAddrMiddleware()

        remote.process_request(request)

        with self.assertRaises(KeyError):
            request.META['REMOTE_ADDR']
