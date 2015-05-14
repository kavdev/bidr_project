# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bids', '0003_auto_20150204_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='amount',
            field=models.IntegerField(verbose_name='Bid Amount'),
            preserve_default=True,
        ),
    ]
