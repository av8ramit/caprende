# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-07 16:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_myuser_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(choices=[(b'LSAT', b'LSAT'), (b'GRE', b'GRE')], max_length=120, verbose_name='Course')),
                ('motivational_image', models.FileField(blank=True, null=True, upload_to=users.utils.upload_location)),
                ('university', models.CharField(choices=[(b'CAL', b'UC Berkeley'), (b'UCLA', b'UCLA'), (b'UCD', b'UC Davis'), (b'UCI', b'UC Irvine'), (b'UCSC', b'UC Santa Cruz'), (b'UCSD', b'UC San Diego'), (b'UCSB', b'UC Santa Barbara'), (b'UCR', b'UC Riverside'), (b'UCM', b'UC Merced'), (b'SJSU', b'San Jose State'), (b'Harvard', b'Harvard'), (b'Princeton', b'Princeton'), (b'Columbia', b'Columbia'), (b'Cornell', b'Cornell'), (b'Yale', b'Yale'), (b'Brown', b'Brown'), (b'Dartmouth', b'Dartmouth'), (b'UPENN', b'University of Pennsylvania'), (b'Duke', b'Duke'), (b'Unlisted', b'Unlisted University')], default='Other', max_length=100)),
                ('major', models.CharField(choices=[(b'ARTS', b'Arts and Humanities'), (b'BUSINESS', b'Accounting, Finance, and Business'), (b'LGS', b'Legal Studies'), (b'HEALTH_MEDICINE', b'Public Health and Medicine'), (b'IDS', b'Multi-/Interdisciplinary Studies'), (b'PSS', b'Public and Social Services'), (b'STM', b'Science and Math'), (b'ENG', b'Engineering'), (b'SS', b'Social Science'), (b'TPS', b'Trades and Personal Services'), (b'OTHER_MAJOR', b'Unlisted Major')], default='Unlisted University', max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='Email Address'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
