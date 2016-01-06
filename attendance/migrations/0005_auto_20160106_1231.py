# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_auto_20160106_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='entry_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='entry_time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]
