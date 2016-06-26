# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-23 19:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20160622_2137'),
    ]

    operations = [
        migrations.RenameField(
            model_name='decision',
            old_name='FactsAndSubmissions',
            new_name='Facts',
        ),
        migrations.AddField(
            model_name='decision',
            name='FactsHeader',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='decision',
            name='OrderHeader',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='decision',
            name='ReasonsHeader',
            field=models.TextField(default=''),
        ),
    ]
