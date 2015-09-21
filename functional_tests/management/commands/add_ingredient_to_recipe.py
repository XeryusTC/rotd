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
from django.core.management.base import BaseCommand, CommandError
from recipes.models import Recipe, Ingredient, IngredientUsage

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ingredient_pk')
        parser.add_argument('recipe_slug')
        parser.add_argument('-q', '--quantity', type=int, const=1, default=1,
                nargs='?')

    def handle(self, *args, **options):
        try:
            r = Recipe.objects.get(slug=options['recipe_slug'])
        except Recipe.DoesNotExist:
            raise CommandError('No recipe with slug "{}"'.format(
                options['recipe_slug']))

        try:
            i = Ingredient.objects.get(pk=options['ingredient_pk'])
        except Ingredient.DoesNotExist:
            raise CommandError('Ingredient {} does not exist'.format(
                options['ingredient_pk']))

        u = IngredientUsage(recipe=r, ingredient=i,
                quantity=options['quantity'])
        u.full_clean()
        u.save()
