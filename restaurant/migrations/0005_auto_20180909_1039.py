# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-09 10:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_auto_20180902_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='modifier',
            name='modifier_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='secondarymodifier',
            name='secondary_modifier_name',
            field=models.CharField(max_length=100),
        ),
    ]
