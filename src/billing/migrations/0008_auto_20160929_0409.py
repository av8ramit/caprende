# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-29 04:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0007_auto_20160929_0408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='date_ended',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 29, 4, 9, 26, 85968, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='membership',
            name='date_start',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 29, 4, 9, 26, 86230, tzinfo=utc)),
        ),
    ]
