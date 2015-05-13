# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20150429_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='note',
            field=models.TextField(default=None, null=True),
            preserve_default=True,
        ),
    ]
