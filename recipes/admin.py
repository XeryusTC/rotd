from django.contrib import admin

from rotd.admin import admin_site
from recipes.models import Recipe

admin_site.register(Recipe)
