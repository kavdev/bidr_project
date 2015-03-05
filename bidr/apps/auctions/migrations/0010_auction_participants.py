# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auctions', '0009_auto_20150303_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='participants',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='participants', blank=True, verbose_name='Participants'),
            preserve_default=True,
        ),
    ]
