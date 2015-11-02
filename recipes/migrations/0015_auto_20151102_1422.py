# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_auto_20151102_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='add_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
