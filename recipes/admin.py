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

from django.contrib import admin

from common.admin import admin_site
from recipes.models import Recipe, Ingredient, IngredientUsage

class IngredientInline(admin.TabularInline):
    model = IngredientUsage

@admin.register(Recipe, site=admin_site)
class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ IngredientInline ]

@admin.register(Ingredient, site=admin_site)
class IngredientAdmin(admin.ModelAdmin):
    pass
