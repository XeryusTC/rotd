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

import datetime
from django.core.urlresolvers import reverse_lazy
from django.http.response import Http404
from django.shortcuts import render
from django.views.generic import FormView, TemplateView, DetailView

from recipes.forms import ContactForm
from recipes.models import Recipe

def todays_recipe(day=datetime.date.today()):
    try:
        li = Recipe.objects.filter(add_date__lt=datetime.date.today()
                ).order_by('id')
        return li[(day.month * day.day + day.year) % len(li)]
    except ZeroDivisionError:
        pass

class ContactView(FormView):
    template_name = 'recipes/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('recipes:contact_thanks')

    def form_valid(self, form):
        form.send_mail()
        return super(ContactView, self).form_valid(form)

class ContactThanksView(TemplateView):
    template_name = 'recipes/contact_thanks.html'

class RecipeDetailView(DetailView):
    model = Recipe

    def get(self, request, **kwargs):
        try:
            return super(DetailView, self).get(request, **kwargs)
        except (Http404, AttributeError):
            return render(request, 'recipes/recipe_detail.html',
                    {'recipe': todays_recipe(), 'is_homepage': True})
