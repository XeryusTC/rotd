# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_auto_20150919_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='type',
            field=models.CharField(max_length=2, choices=[('gr', 'gram'), ('cL', 'centiliter'), ('co', 'teen')], blank=True),
        ),
    ]
