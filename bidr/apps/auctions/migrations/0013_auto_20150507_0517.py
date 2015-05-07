# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auction_bid_increments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='bid_increments',
        ),
        migrations.AddField(
            model_name='auction',
            name='bid_increment',
            field=models.DecimalField(verbose_name='Bid Increment', decimal_places=2, null=True, blank=True, max_digits=10),
            preserve_default=True,
        ),
    ]
