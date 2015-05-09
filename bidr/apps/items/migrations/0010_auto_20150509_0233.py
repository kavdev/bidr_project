# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0009_auto_20150509_0212'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='minimum_price',
            new_name='starting_bid',
        ),
    ]
