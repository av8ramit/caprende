# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-21 06:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_userprofile_next_question_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course'),
        ),
    ]