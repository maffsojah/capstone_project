# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 14:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_auto_20170313_1413'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='services',
            name='id',
        ),
        migrations.AlterField(
            model_name='services',
            name='Customer_ID',
            field=models.IntegerField(default=True, primary_key=True, serialize=False),
        ),
    ]