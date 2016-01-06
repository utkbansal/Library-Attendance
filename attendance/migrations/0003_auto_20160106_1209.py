# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_auto_20151002_1252'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendance',
            options={'ordering': ['entry_datetime', 'exit_datetime'], 'verbose_name_plural': 'Attendance'},
        ),
        migrations.RenameField(
            model_name='attendance',
            old_name='entry_time',
            new_name='entry_datetime',
        ),
        migrations.RenameField(
            model_name='attendance',
            old_name='exit_time',
            new_name='exit_datetime',
        ),
    ]
