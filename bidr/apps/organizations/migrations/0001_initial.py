# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20150205_1130'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('email', models.EmailField(max_length=75, blank=True, verbose_name='Email Address', unique=True)),
                ('phone_number', models.CharField(verbose_name='Phone Number', max_length=20)),
                ('website', models.URLField(verbose_name='Website')),
                ('auctions', models.ManyToManyField(to='auctions.Auction')),
                ('managers', models.ManyToManyField(verbose_name='Manager', to=settings.AUTH_USER_MODEL, related_name='managers')),
                ('owner', models.ForeignKey(verbose_name='Admin', related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
