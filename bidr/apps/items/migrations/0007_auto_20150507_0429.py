# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_auto_20150307_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractitem',
            name='description',
            field=models.TextField(blank=True, max_length=80),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='minimum_price',
            field=models.DecimalField(validators=[django.core.validators.MinValueValidator(0)], max_digits=7, default=0, decimal_places=2),
            preserve_default=True,
        ),
    ]
