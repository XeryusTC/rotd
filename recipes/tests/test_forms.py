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

from django.core import mail
from django.test import TestCase

from recipes.forms import ContactForm

class ContactFormTests(TestCase):
    def send_test_mail(self):
        form = ContactForm({'name': 'Test Case', 'email': 'test@test.test',
            'subject': 'Test subject', 'body': 'Test body'})
        # Validate the data so we know it's safe and stored appropiatly,
        # the assertion is there just to make sure
        self.assertTrue(form.is_valid())

        form.send_mail()

    def test_name_email_subject_body_fields_required(self):
        form = ContactForm({'name': ''})
        self.assertFalse(form.is_valid())

        # Check if required by just checking whether errors were raised
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('subject', form.errors)
        self.assertIn('body', form.errors)

    def test_form_sends_mail(self):
        self.send_test_mail()
        self.assertEqual(len(mail.outbox), 1)

    def test_mail_contains_all_information(self):
        self.send_test_mail()
        self.assertIn('Test Case', mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].from_email, 'test@test.test')
        self.assertIn('Test subject', mail.outbox[0].subject)
        self.assertIn('Test body', mail.outbox[0].body)
