# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-24 22:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20160625_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decision',
            name='Distribution',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'D'), ('D', 'D')], default='', max_length=1),
        ),
    ]
