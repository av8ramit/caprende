# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-01 06:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0013_auto_20160527_0619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='passage',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
    ]
