# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auctions', '0004_auto_20150205_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='managers',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Managers', related_name='auction_managers'),
            preserve_default=True,
        ),
    ]
