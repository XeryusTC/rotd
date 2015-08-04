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

from django import forms
from django.core.mail import send_mail

class ContactForm(forms.Form):
    name = forms.CharField(label='Naam', required=True)
    email = forms.EmailField(label='Email', required=True)
    subject = forms.CharField(label='Onderwerp', required=True)
    body = forms.CharField(label='Boodschap', required=True,
            widget=forms.widgets.Textarea())

    def send_mail(self):
        data = self.cleaned_data
        body = 'Contact from {name}:\n\n{body}'.format(name=data['name'],
            body=data['body'])
        subject = '[Contact form] {}'.format(data['subject'])
        send_mail(subject, body, data['email'],
            ['contact@watzalikvanavondeten.nl'], fail_silently=True)
