# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auction_participants'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Start Time'),
            preserve_default=True,
        ),
    ]
