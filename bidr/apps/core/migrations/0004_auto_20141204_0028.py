# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20141204_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidder',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, verbose_name='Phone Number'),
        ),
    ]
