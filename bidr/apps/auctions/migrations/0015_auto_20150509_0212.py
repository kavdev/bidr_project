# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auto_20150507_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='bid_increment',
            field=models.DecimalField(max_digits=17, decimal_places=2, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Bid Increment', default=Decimal('0.01')),
            preserve_default=True,
        ),
    ]
