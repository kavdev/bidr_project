# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0013_auto_20150514_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='starting_bid',
            field=models.BigIntegerField(validators=[django.core.validators.MinValueValidator(0)], default=0),
            preserve_default=True,
        ),
    ]
