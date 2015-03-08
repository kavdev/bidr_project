# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0005_auto_20150305_0322'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='min_price',
            new_name='minimum_price',
        ),
    ]
