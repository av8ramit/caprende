# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-15 20:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20160515_0223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursesection',
            name='description',
            field=models.TextField(default='', max_length=10000, null=True),
        ),
    ]
