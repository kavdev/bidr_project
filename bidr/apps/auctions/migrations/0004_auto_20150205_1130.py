# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auction_optional_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='item_collections',
            field=models.ManyToManyField(blank=True, verbose_name='Collections of Items', to='items.ItemCollection'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='items',
            field=models.ManyToManyField(blank=True, verbose_name='Items', to='items.Item'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='user_info',
            field=models.ManyToManyField(blank=True, verbose_name='Additional User Info', to='auctions.AuctionUserInfo'),
        ),
    ]
