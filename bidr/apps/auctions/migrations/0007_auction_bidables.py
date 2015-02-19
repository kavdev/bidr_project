# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20150216_1806'),
        ('items', '0002_auto_20150216_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='bidables',
            field=models.ManyToManyField(verbose_name='Bidables', to='items.AbstractItem', blank=True),
            preserve_default=True,
        ),
    ]
