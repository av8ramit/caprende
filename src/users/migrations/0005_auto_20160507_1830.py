# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-07 18:30
from __future__ import unicode_literals

from django.db import migrations, models
import users.utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20160507_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='image',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='last_name',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_image',
            field=models.FileField(blank=True, null=True, upload_to=users.utils.upload_location, verbose_name='Profile Picture'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='course',
            field=models.CharField(blank=True, choices=[(b'LSAT', b'LSAT'), (b'GRE', b'GRE')], max_length=120, verbose_name='Course'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='major',
            field=models.CharField(blank=True, choices=[(b'ARTS', b'Arts and Humanities'), (b'BUSINESS', b'Accounting, Finance, and Business'), (b'LGS', b'Legal Studies'), (b'HEALTH_MEDICINE', b'Public Health and Medicine'), (b'IDS', b'Multi-/Interdisciplinary Studies'), (b'PSS', b'Public and Social Services'), (b'STM', b'Science and Math'), (b'ENG', b'Engineering'), (b'SS', b'Social Science'), (b'TPS', b'Trades and Personal Services'), (b'OTHER_MAJOR', b'Unlisted Major')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='motivational_image',
            field=models.FileField(blank=True, null=True, upload_to=users.utils.upload_location, verbose_name='Motivational Image'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='university',
            field=models.CharField(blank=True, choices=[(b'CAL', b'UC Berkeley'), (b'UCLA', b'UCLA'), (b'UCD', b'UC Davis'), (b'UCI', b'UC Irvine'), (b'UCSC', b'UC Santa Cruz'), (b'UCSD', b'UC San Diego'), (b'UCSB', b'UC Santa Barbara'), (b'UCR', b'UC Riverside'), (b'UCM', b'UC Merced'), (b'SJSU', b'San Jose State'), (b'Harvard', b'Harvard'), (b'Princeton', b'Princeton'), (b'Columbia', b'Columbia'), (b'Cornell', b'Cornell'), (b'Yale', b'Yale'), (b'Brown', b'Brown'), (b'Dartmouth', b'Dartmouth'), (b'UPENN', b'University of Pennsylvania'), (b'Duke', b'Duke'), (b'Unlisted', b'Unlisted University')], max_length=100, null=True),
        ),
    ]
