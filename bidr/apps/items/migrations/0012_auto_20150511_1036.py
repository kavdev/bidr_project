# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0011_auto_20150511_0344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractitem',
            name='polymorphic_ctype',
            field=models.ForeignKey(null=True, related_name='polymorphic_items.abstractitem_set+', editable=False, to='contenttypes.ContentType'),
            preserve_default=True,
        ),
    ]
