# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_recipe_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='add_date',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2015, 7, 22, 13, 40, 19, 118467, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
