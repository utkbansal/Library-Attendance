# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry_time', models.DateTimeField()),
                ('exit_time', models.DateTimeField(default=None, null=True)),
                ('student_number', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='attendance',
            name='room',
            field=models.ForeignKey(to='attendance.Room'),
        ),
    ]
