# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='Name', max_length=100)),
                ('slug', models.SlugField(verbose_name='Slug', max_length=120, unique=True)),
                ('email', models.EmailField(verbose_name='Email Address', blank=True, null=True, max_length=75)),
                ('phone_number', models.CharField(verbose_name='Phone Number', blank=True, null=True, max_length=20)),
                ('website', models.URLField(verbose_name='Website', blank=True, null=True)),
                ('auctions', models.ManyToManyField(related_name='auctions', to='auctions.Auction', verbose_name='Auctions', blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Owner', related_name='owner')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
