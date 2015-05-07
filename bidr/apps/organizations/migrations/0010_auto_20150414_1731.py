# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0009_remove_organization_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='email',
            field=models.EmailField(blank=True, verbose_name='Email Address', null=True, max_length=75),
            preserve_default=True,
        ),
    ]
