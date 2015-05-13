# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20150429_0123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='user',
        ),
        migrations.RemoveField(
            model_name='ticketpost',
            name='thread',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
        migrations.RemoveField(
            model_name='ticketpost',
            name='user',
        ),
        migrations.DeleteModel(
            name='TicketPost',
        ),
    ]
