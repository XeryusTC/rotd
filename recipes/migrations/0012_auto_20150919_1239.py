# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_remove_ingredient_used_in'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='used_in2',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='used_in',
            field=models.ManyToManyField(related_name='ingredient_set', blank=True, to='recipes.Recipe', through='recipes.IngredientUsage'),
        ),
    ]
