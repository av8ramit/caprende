# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-01 04:31
from __future__ import unicode_literals

from django.db import migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20160721_0646'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='state',
            field=localflavor.us.models.USStateField(blank=True, null=True),
        ),
    ]
