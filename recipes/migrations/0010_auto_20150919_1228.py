# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def change_to_usage(apps, schema_editor):
    Recipe = apps.get_model("recipes", "Recipe")
    Ingredient = apps.get_model("recipes", "Ingredient")
    IngredientUsage = apps.get_model("recipes", "IngredientUsage")

    for recipe in Recipe.objects.all():
        for ingredient in recipe.ingredient_set.all():
            u = IngredientUsage(recipe=r, ingredient=i, quantity=1)
            u.save()

class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_auto_20150919_1226'),
    ]

    operations = [
        migrations.RunPython(change_to_usage),
    ]
