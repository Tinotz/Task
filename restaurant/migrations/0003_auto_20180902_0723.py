# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-02 07:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_auto_20180902_0702'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='Restaurant',
            new_name='restaurant',
        ),
    ]
