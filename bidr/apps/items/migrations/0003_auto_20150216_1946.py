# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bids', '0003_auto_20150204_2137'),
        ('items', '0002_auto_20150216_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abstractitem',
            name='bid',
        ),
        migrations.AddField(
            model_name='abstractitem',
            name='bids',
            field=models.ManyToManyField(to='bids.Bid', blank=True, related_name='bids', verbose_name='Bids'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='abstractitem',
            name='claimed_bid',
            field=models.ForeignKey(to='bids.Bid', null=True, blank=True, verbose_name='Claimed Bid'),
            preserve_default=True,
        ),
    ]
