# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0002_auto_20150429_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='reference',
            field=models.CharField(default='1234-ABCD', max_length=24),
            preserve_default=False,
        ),
    ]
