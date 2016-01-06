# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_auto_20160106_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='entry_time',
            field=models.TimeField(null=True, default=None),
        ),
        migrations.AddField(
            model_name='attendance',
            name='exit_time',
            field=models.TimeField(null=True, default=None),
        ),
    ]
