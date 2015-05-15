# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidruser',
            name='display_name',
            field=models.CharField(default='Anonymous', max_length=30, verbose_name='Display Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bidruser',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Full Name'),
            preserve_default=True,
        ),
    ]
