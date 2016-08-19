# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-13 19:37
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ended', models.DateTimeField(default=datetime.datetime(2016, 8, 13, 19, 37, 4, 169218, tzinfo=utc))),
                ('date_start', models.DateTimeField(default=datetime.datetime(2016, 8, 13, 19, 37, 4, 169509, tzinfo=utc))),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=120)),
                ('order_id', models.CharField(max_length=120)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('success', models.BooleanField(default=True)),
                ('transaction_status', models.CharField(blank=True, max_length=220, null=True)),
                ('card_type', models.CharField(max_length=120)),
                ('last_four', models.PositiveIntegerField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='UserMerchantId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(max_length=120)),
                ('subscription_id', models.CharField(blank=True, max_length=120, null=True)),
                ('plan_id', models.CharField(blank=True, max_length=120, null=True)),
                ('merchant_name', models.CharField(default='Braintree', max_length=120)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
