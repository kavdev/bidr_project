# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='auctions',
            field=models.ManyToManyField(related_name='auctions', verbose_name='Auctions', to='auctions.Auction'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='managers',
            field=models.ManyToManyField(related_name='managers', verbose_name='Managers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='organization',
            name='owner',
            field=models.ForeignKey(related_name='owner', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
    ]
