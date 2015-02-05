# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20150204_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='optional_password',
            field=models.CharField(verbose_name='Password', max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
    ]
