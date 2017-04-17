# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-17 02:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0012_auto_20170415_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='service',
            field=models.ForeignKey(db_column='service_no', null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.Service'),
        ),
    ]