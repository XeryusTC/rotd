# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.template.defaultfilters import slugify

def slugify_name(apps, schema_editor):
    Recipe = apps.get_model('recipes', 'Recipe')
    for r in Recipe.objects.all():
        r.slug = slugify(r.name)
        r.save()

class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_recipe_add_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(default=''),
        ),
        migrations.RunPython(slugify_name),
    ]
