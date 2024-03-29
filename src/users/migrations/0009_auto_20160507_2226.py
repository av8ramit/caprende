# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-07 22:26
from __future__ import unicode_literals

from django.db import migrations, models
import users.utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20160507_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='motivational_image',
            field=models.FileField(blank=True, default='', null=True, upload_to=users.utils.upload_location, verbose_name='img/college.jpg'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.FileField(blank=True, default='img/profile.jpg', null=True, upload_to=users.utils.upload_location, verbose_name='Profile Picture'),
        ),
    ]
