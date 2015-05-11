# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0010_auto_20150509_0233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractitem',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_items.abstractitem_set', to='contenttypes.ContentType', null=True, editable=False),
            preserve_default=True,
        ),
    ]
