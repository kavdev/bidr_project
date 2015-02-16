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
            field=models.ManyToManyField(related_name='auctions', blank=True, verbose_name='Auctions', to='auctions.Auction'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='managers',
            field=models.ManyToManyField(related_name='managers', blank=True, verbose_name='Managers', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
