# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_category_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='is_main_image',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
