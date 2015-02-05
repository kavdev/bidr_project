# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='item_collections',
            field=models.ManyToManyField(to='items.ItemCollection', verbose_name='Collections of Items'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='auction',
            name='items',
            field=models.ManyToManyField(to='items.Item', verbose_name='Items'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='auction',
            name='user_info',
            field=models.ManyToManyField(to='auctions.AuctionUserInfo', verbose_name='Additional User Info'),
            preserve_default=True,
        ),
    ]
