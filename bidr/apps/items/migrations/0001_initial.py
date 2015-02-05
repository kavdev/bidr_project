# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('bids', '0003_auto_20150204_2137'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=60)),
                ('description', models.TextField()),
                ('min_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('picture', models.ImageField(upload_to='')),
                ('bid', models.ForeignKey(to='bids.Bid', verbose_name='Bid')),
                ('tags', taggit.managers.TaggableManager(through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags', help_text='A comma-separated list of tags.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemCollection',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=60)),
                ('description', models.TextField()),
                ('bid', models.ForeignKey(to='bids.Bid', verbose_name='Bid')),
                ('items', models.ManyToManyField(to='items.Item', verbose_name='Items')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
