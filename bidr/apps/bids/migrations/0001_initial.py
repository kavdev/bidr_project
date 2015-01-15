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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(verbose_name='Bid Amount', decimal_places=2, max_digits=40)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
            ],
            options={
                'verbose_name': 'Bid',
            },
            bases=(models.Model,),
        ),
    ]
