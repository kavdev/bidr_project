# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('amount', models.BigIntegerField(verbose_name='Bid Amount')),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp', auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
