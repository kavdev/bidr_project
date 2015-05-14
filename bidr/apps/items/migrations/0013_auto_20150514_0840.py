# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0012_auto_20150511_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='starting_bid',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=True,
        ),
    ]
