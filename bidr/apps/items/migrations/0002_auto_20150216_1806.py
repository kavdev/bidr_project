# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bids', '0003_auto_20150204_2137'),
        ('contenttypes', '0001_initial'),
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('description', models.TextField()),
                ('claimed', models.BooleanField(default=False)),
                ('bid', models.ForeignKey(verbose_name='Bid', to='bids.Bid')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, related_name='polymorphic_items.abstractitem_set', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='item',
            name='bid',
        ),
        migrations.RemoveField(
            model_name='item',
            name='description',
        ),
        migrations.RemoveField(
            model_name='item',
            name='id',
        ),
        migrations.RemoveField(
            model_name='item',
            name='title',
        ),
        migrations.RemoveField(
            model_name='itemcollection',
            name='bid',
        ),
        migrations.RemoveField(
            model_name='itemcollection',
            name='description',
        ),
        migrations.RemoveField(
            model_name='itemcollection',
            name='id',
        ),
        migrations.RemoveField(
            model_name='itemcollection',
            name='name',
        ),
        migrations.AddField(
            model_name='item',
            name='abstractitem_ptr',
            field=models.OneToOneField(to='items.AbstractItem', serialize=False, auto_created=True, default=1, parent_link=True, primary_key=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itemcollection',
            name='abstractitem_ptr',
            field=models.OneToOneField(to='items.AbstractItem', serialize=False, auto_created=True, default=1, parent_link=True, primary_key=True),
            preserve_default=False,
        ),
    ]
