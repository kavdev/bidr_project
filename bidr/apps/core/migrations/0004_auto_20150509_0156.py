# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150304_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidruser',
            name='phone_number',
            field=models.CharField(max_length=20, verbose_name='Phone Number'),
            preserve_default=True,
        ),
    ]
