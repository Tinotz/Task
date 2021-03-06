# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-02 09:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_auto_20180902_0723'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='name',
            new_name='item_name',
        ),
        migrations.RenameField(
            model_name='modifier',
            old_name='name',
            new_name='modifier_name',
        ),
        migrations.RenameField(
            model_name='restaurant',
            old_name='name',
            new_name='restaurant_name',
        ),
        migrations.RenameField(
            model_name='secondarymodifier',
            old_name='name',
            new_name='secondary_modifier_name',
        ),
    ]
