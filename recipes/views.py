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
from django.shortcuts import render

from recipes.models import Recipe

def todays_recipe(day=datetime.date.today()):
    try:
        target = (day.month * day.day + day.year) % \
            Recipe.objects.filter(add_date__lt=datetime.date.today()).count()
        return Recipe.objects.all()[target]
    except:
        pass

def home_page(request):
    recipe = todays_recipe()
    return render(request, 'recipes/home.html', {'recipe': recipe})
