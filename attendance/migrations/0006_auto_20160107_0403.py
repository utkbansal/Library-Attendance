# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_auto_20160106_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='entry_datetime',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='entry_time',
            field=models.TimeField(auto_now=True),
        ),
    ]
