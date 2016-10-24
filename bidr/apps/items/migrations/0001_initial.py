# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('contenttypes', '0001_initial'),
        ('bids', '0002_bid_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractItem',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('description', models.TextField(max_length=300, blank=True)),
                ('claimed', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('abstractitem_ptr', models.OneToOneField(serialize=False, parent_link=True, to='items.AbstractItem',
                                                          auto_created=True, primary_key=True)),
                ('starting_bid', models.BigIntegerField(validators=[django.core.validators.MinValueValidator(0)],
                                                        default=0)),
                ('picture', models.ImageField(upload_to='', null=True, blank=True)),
                ('tags', taggit.managers.TaggableManager(
                    to='taggit.Tag', verbose_name='Tags',
                    help_text='A comma-separated list of tags.', through='taggit.TaggedItem')),
            ],
            options={
                'abstract': False,
            },
            bases=('items.abstractitem',),
        ),
        migrations.CreateModel(
            name='ItemCollection',
            fields=[
                ('abstractitem_ptr', models.OneToOneField(serialize=False, parent_link=True, to='items.AbstractItem',
                                                          auto_created=True, primary_key=True)),
                ('items', models.ManyToManyField(to='items.Item', verbose_name='Items', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('items.abstractitem',),
        ),
        migrations.AddField(
            model_name='abstractitem',
            name='bids',
            field=models.ManyToManyField(related_name='bids', to='bids.Bid', verbose_name='Bids', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='abstractitem',
            name='claimed_bid',
            field=models.ForeignKey(to='bids.Bid', verbose_name='Claimed Bid', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='abstractitem',
            name='polymorphic_ctype',
            field=models.ForeignKey(to='contenttypes.ContentType', related_name='polymorphic_items.abstractitem_set+',
                                    null=True, editable=False),
            preserve_default=True,
        ),
    ]
