# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bids', '0004_auto_20150514_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='amount',
            field=models.BigIntegerField(verbose_name='Bid Amount'),
            preserve_default=True,
        ),
    ]
