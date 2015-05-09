# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0008_auto_20150507_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='minimum_price',
            field=models.DecimalField(max_digits=17, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)], default=0),
            preserve_default=True,
        ),
    ]
