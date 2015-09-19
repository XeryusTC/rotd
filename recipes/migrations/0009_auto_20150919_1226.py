# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20150904_2127'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientUsage',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('ingredient', models.ForeignKey(to='recipes.Ingredient')),
                ('recipe', models.ForeignKey(to='recipes.Recipe')),
            ],
        ),
        migrations.AddField(
            model_name='ingredient',
            name='used_in2',
            field=models.ManyToManyField(blank=True, to='recipes.Recipe', related_name='ingredients', through='recipes.IngredientUsage'),
        ),
    ]
