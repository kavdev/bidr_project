# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_bidruser_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidruser',
            name='email',
            field=models.EmailField(max_length=75, verbose_name='Email Address', unique=True),
            preserve_default=True,
        ),
    ]
