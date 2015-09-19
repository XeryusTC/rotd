# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_auto_20150919_1228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='used_in',
        ),
    ]
