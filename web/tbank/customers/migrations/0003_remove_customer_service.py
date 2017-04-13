# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_auto_20170402_1821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='service',
        ),
    ]
