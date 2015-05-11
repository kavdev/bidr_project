# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_bidruser_ios_device_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidruser',
            name='ios_device_token',
            field=models.CharField(verbose_name='iOS Device Token', blank=True, max_length=64, null=True),
            preserve_default=True,
        ),
    ]
