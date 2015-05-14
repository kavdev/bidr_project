# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='Name', max_length=60)),
                ('description', models.TextField(verbose_name='Description')),
                ('start_time', models.DateTimeField(verbose_name='Start Time', blank=True, null=True)),
                ('end_time', models.DateTimeField(verbose_name='End Time')),
                ('optional_password', models.CharField(verbose_name='Password', blank=True, null=True, max_length=128)),
                ('bid_increment', models.BigIntegerField(verbose_name='Bid Increment', validators=[django.core.validators.MinValueValidator(1)], default=1)),
                ('stage', models.PositiveSmallIntegerField(verbose_name='Auction Stage', default=0, choices=[(0, 'Plan'), (1, 'Observe'), (2, 'Claim'), (3, 'Report')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
