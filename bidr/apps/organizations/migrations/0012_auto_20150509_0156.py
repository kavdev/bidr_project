# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0011_auto_20150509_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='phone_number',
            field=models.CharField(max_length=20, null=True, blank=True, verbose_name='Phone Number'),
            preserve_default=True,
        ),
    ]
