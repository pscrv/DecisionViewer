# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-11 13:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20160611_0032'),
    ]

    operations = [
        migrations.RenameField(
            model_name='decision',
            old_name='DecisionDate',
            new_name='_DecisionDate',
        ),
        migrations.RenameField(
            model_name='decision',
            old_name='OnlineDate',
            new_name='_OnlineDate',
        ),
        migrations.RenameField(
            model_name='decision',
            old_name='Text',
            new_name='_Text',
        ),
    ]
