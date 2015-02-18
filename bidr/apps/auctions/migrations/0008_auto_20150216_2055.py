# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auction_bidables'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='bidables',
            field=models.ManyToManyField(verbose_name='Bidables', blank=True, to='items.AbstractItem', related_name='bidables'),
            preserve_default=True,
        ),
    ]
