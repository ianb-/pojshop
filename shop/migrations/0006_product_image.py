# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_productimage_is_main_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ForeignKey(related_name='cover_photo', blank=True, to='shop.ProductImage', null=True),
            preserve_default=True,
        ),
    ]
