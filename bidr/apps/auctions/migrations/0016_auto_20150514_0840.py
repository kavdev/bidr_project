# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_auto_20150509_0212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='bid_increment',
            field=models.IntegerField(verbose_name='Bid Increment', default=1, validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=True,
        ),
    ]
