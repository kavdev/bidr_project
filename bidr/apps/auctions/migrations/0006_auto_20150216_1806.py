# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auction_managers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='item_collections',
        ),
        migrations.RemoveField(
            model_name='auction',
            name='items',
        ),
    ]
