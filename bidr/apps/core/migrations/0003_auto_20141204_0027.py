# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20141204_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidder',
            name='phone_number',
            field=models.CharField(max_length=30, blank=True, verbose_name='Phone Number'),
        ),
    ]
