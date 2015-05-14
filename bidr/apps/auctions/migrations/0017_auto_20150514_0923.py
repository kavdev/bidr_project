# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20150514_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='bid_increment',
            field=models.BigIntegerField(validators=[django.core.validators.MinValueValidator(1)], default=1, verbose_name='Bid Increment'),
            preserve_default=True,
        ),
    ]
