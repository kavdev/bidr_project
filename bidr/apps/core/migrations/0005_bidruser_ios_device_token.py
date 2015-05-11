# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150509_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidruser',
            name='ios_device_token',
            field=models.CharField(max_length=64, blank=True, verbose_name='iOS Device Token'),
            preserve_default=True,
        ),
    ]
