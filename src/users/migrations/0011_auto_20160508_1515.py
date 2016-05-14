# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-08 15:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20160507_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='major',
            field=models.CharField(blank=True, choices=[(b'Arts and Humanities', b'Arts and Humanities'), (b'Accounting, Finance, and Business', b'Accounting, Finance, and Business'), (b'Legal Studies', b'Legal Studies'), (b'Public Health and Medicine', b'Public Health and Medicine'), (b'Multi-/Interdisciplinary Studies', b'Multi-/Interdisciplinary Studies'), (b'Public and Social Services', b'Public and Social Services'), (b'Science and Math', b'Science and Math'), (b'Engineering', b'Engineering'), (b'Social Science', b'Social Science'), (b'Trades and Personal Services', b'Trades and Personal Services'), (b'Unlisted Major', b'Unlisted Major')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='university',
            field=models.CharField(blank=True, choices=[(b'UC Berkeley', b'UC Berkeley'), (b'UCLA', b'UCLA'), (b'UC Davis', b'UC Davis'), (b'UC Irvine', b'UC Irvine'), (b'UC Santa Cruz', b'UC Santa Cruz'), (b'UC San Diego', b'UC San Diego'), (b'UC Santa Barbara', b'UC Santa Barbara'), (b'UC Riverside', b'UC Riverside'), (b'UC Merced', b'UC Merced'), (b'San Jose State University', b'San Jose State'), (b'Harvard', b'Harvard'), (b'Princeton', b'Princeton'), (b'Columbia', b'Columbia'), (b'Cornell', b'Cornell'), (b'Yale', b'Yale'), (b'Brown', b'Brown'), (b'Dartmouth', b'Dartmouth'), (b'University of Pennsylvania', b'University of Pennsylvania'), (b'Duke', b'Duke'), (b'Unlisted University', b'Unlisted University')], max_length=100, null=True),
        ),
    ]
