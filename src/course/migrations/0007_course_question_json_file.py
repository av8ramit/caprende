# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-19 05:40
from __future__ import unicode_literals

import course.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_auto_20160719_0458'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='question_json_file',
            field=models.FileField(blank=True, null=True, upload_to=course.utils.upload_location),
        ),
    ]
