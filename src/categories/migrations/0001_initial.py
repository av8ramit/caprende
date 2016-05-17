# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-15 20:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0004_auto_20160515_2023'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('slug', models.SlugField(default='default-slug', unique=True)),
                ('description', models.TextField(default='', max_length=2000, null=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.CourseSection')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField(default='default-slug', unique=True)),
                ('description', models.TextField(default='', max_length=2000, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.Category')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('section', 'name')]),
        ),
    ]
