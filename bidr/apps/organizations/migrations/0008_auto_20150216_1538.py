# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0007_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='email',
            field=models.EmailField(null=True, verbose_name='Email Address', unique=True, max_length=75, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='phone_number',
            field=models.CharField(null=True, verbose_name='Phone Number', max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='website',
            field=models.URLField(null=True, verbose_name='Website', blank=True),
        ),
    ]
