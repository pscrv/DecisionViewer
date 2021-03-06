# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-22 19:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20160621_2359'),
    ]

    operations = [
        migrations.RenameField(
            model_name='decision',
            old_name='Language',
            new_name='DecisionLanguage',
        ),
        migrations.RenameField(
            model_name='decision',
            old_name='FactsAndSubmissions_DE',
            new_name='FactsAndSubmissions',
        ),
        migrations.RenameField(
            model_name='decision',
            old_name='FactsAndSubmissions_EN',
            new_name='Order',
        ),
        migrations.RenameField(
            model_name='decision',
            old_name='FactsAndSubmissions_FR',
            new_name='Reasons',
        ),
        migrations.RemoveField(
            model_name='decision',
            name='Order_DE',
        ),
        migrations.RemoveField(
            model_name='decision',
            name='Order_EN',
        ),
        migrations.RemoveField(
            model_name='decision',
            name='Order_FR',
        ),
        migrations.RemoveField(
            model_name='decision',
            name='Reasons_DE',
        ),
        migrations.RemoveField(
            model_name='decision',
            name='Reasons_EN',
        ),
        migrations.RemoveField(
            model_name='decision',
            name='Reasons_FR',
        ),
        migrations.AddField(
            model_name='decision',
            name='ProcedureLanguage',
            field=models.CharField(default='', max_length=2),
        ),
    ]
