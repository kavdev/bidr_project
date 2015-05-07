# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auction_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='bid_increments',
            field=models.DecimalField(blank=True, null=True, max_digits=10, verbose_name='Bid Increments', decimal_places=2),
            preserve_default=True,
        ),
    ]
