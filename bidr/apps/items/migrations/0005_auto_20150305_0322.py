# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_auto_20150218_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemcollection',
            name='items',
            field=models.ManyToManyField(verbose_name='Items', to='items.Item', blank=True),
            preserve_default=True,
        ),
    ]
