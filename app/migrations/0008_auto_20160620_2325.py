# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-20 21:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_decision_metadownloaded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decision',
            name='ApplicationNumber',
            field=models.CharField(default='', max_length=15),
        ),
    ]