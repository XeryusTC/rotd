# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_ingredient_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='add_date',
            field=models.DateField(editable=False),
        ),
    ]
