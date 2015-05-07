# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0007_auto_20150507_0429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractitem',
            name='description',
            field=models.TextField(blank=True, max_length=300),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abstractitem',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_items.abstractitem_set+', null=True, editable=False, to='contenttypes.ContentType'),
            preserve_default=True,
        ),
    ]
