# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20150507_0517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='bid_increment',
            field=models.DecimalField(max_digits=10, verbose_name='Bid Increment', decimal_places=2, default=Decimal('0.01'), validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
            preserve_default=True,
        ),
    ]
