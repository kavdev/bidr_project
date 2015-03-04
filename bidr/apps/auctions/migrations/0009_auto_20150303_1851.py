# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20150216_2055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='start_time',
        ),
        migrations.AlterField(
            model_name='auction',
            name='stage',
            field=models.PositiveSmallIntegerField(verbose_name='Auction Stage', default=0, choices=[(0, 'Plan'), (1, 'Observe'), (2, 'Claim'), (3, 'Report')]),
            preserve_default=True,
        ),
    ]
