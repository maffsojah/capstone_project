# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-15 07:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0007_auto_20170415_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='Account_Type',
            field=models.IntegerField(choices=[('Cur', 'Current Account'), ('Sav', 'Savings Account')]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='Employer_Stability',
            field=models.IntegerField(choices=[('Unstable', 'Unstable'), ('Stable', 'Stable')]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='Employment',
            field=models.IntegerField(choices=[('Stu', 'Student'), ('Cont', 'Contract'), ('Perm', 'Permanent')]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='Gender',
            field=models.IntegerField(choices=[('M', 'Male'), ('F', 'Female')]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='Residential_Status',
            field=models.IntegerField(choices=[('Rented', 'Rented'), ('Owned', 'Owned')]),
        ),
    ]
