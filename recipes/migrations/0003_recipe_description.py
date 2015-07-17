# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20150717_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
