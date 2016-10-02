# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-29 04:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0008_auto_20160929_0409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='date_ended',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 29, 4, 11, 3, 278981, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='membership',
            name='date_start',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 29, 4, 11, 3, 279309, tzinfo=utc)),
        ),
    ]
