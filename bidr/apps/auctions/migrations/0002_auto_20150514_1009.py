# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('items', '0001_initial'),
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='bidables',
            field=models.ManyToManyField(related_name='bidables', to='items.AbstractItem',
                                         verbose_name='Bidables', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='auction',
            name='managers',
            field=models.ManyToManyField(related_name='auction_managers', to=settings.AUTH_USER_MODEL,
                                         verbose_name='Managers', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='auction',
            name='participants',
            field=models.ManyToManyField(related_name='participants', to=settings.AUTH_USER_MODEL,
                                         verbose_name='Participants', blank=True),
            preserve_default=True,
        ),
    ]
