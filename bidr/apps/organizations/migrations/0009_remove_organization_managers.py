# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0008_auto_20150216_1538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='managers',
        ),
    ]
