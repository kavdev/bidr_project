# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_organization_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='auctions',
            field=models.ManyToManyField(blank=True, to='auctions.Auction', verbose_name='Auctions', related_name='auctions'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='managers',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Managers', related_name='managers'),
        ),
    ]
