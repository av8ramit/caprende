# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-24 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0016_auto_20160624_0445'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='source',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
    ]
