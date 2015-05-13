# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30)),
                ('level', models.PositiveSmallIntegerField(default=3)),
                ('slug', models.SlugField(unique=True)),
                ('details', models.TextField(null=True, blank=True)),
                ('image', models.ImageField(upload_to=b'categories/')),
                ('views', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('parent', models.ForeignKey(blank=True, to='shop.Category', null=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=24)),
                ('firstname', models.CharField(default=None, max_length=32)),
                ('lastname', models.CharField(max_length=32)),
                ('job_title', models.CharField(default=None, max_length=32, null=True, blank=True)),
                ('phone', models.CharField(max_length=12)),
                ('email', models.EmailField(max_length=64)),
                ('notes', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('serial', models.CharField(max_length=64, null=True)),
                ('is_for_sale', models.BooleanField(default=False)),
                ('purchase_price', models.DecimalField(default=None, max_digits=6, decimal_places=2)),
                ('sale_price', models.DecimalField(default=None, null=True, max_digits=6, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('SKU', models.CharField(max_length=64)),
                ('slug', models.SlugField(unique=True)),
                ('details', models.TextField()),
                ('shelf', models.BooleanField(default=False)),
                ('stock', models.PositiveSmallIntegerField(default=0)),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('views', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('sales', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product_to_cat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(to='shop.Category')),
                ('product', models.ForeignKey(to='shop.Product')),
            ],
            options={
                'verbose_name_plural': 'Product Categorisations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'products')),
                ('product', models.ForeignKey(to='shop.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PurchaseDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(max_digits=8, decimal_places=2)),
                ('date', models.DateField()),
                ('final', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SaleDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('quantity', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SaleOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_id', models.CharField(unique=True, max_length=128)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('total_price', models.DecimalField(max_digits=8, decimal_places=2)),
                ('shipping_price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('paid', models.BooleanField(default=False)),
                ('address1', models.CharField(max_length=128)),
                ('address2', models.CharField(max_length=128)),
                ('city', models.CharField(max_length=128)),
                ('county', models.CharField(max_length=128)),
                ('postcode', models.CharField(max_length=8)),
                ('phone', models.CharField(max_length=12)),
                ('shipped', models.NullBooleanField(default=False)),
                ('tracking_number', models.CharField(default=None, max_length=64, null=True)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('address1', models.CharField(max_length=128)),
                ('address2', models.CharField(max_length=128, null=True, blank=True)),
                ('city', models.CharField(max_length=128)),
                ('county', models.CharField(max_length=128)),
                ('postcode', models.CharField(max_length=8)),
                ('phone', models.CharField(max_length=12)),
                ('email', models.EmailField(max_length=64)),
                ('notes', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='saledetail',
            name='order',
            field=models.ForeignKey(to='shop.SaleOrder'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='saledetail',
            name='product',
            field=models.ForeignKey(to='shop.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='supplier',
            field=models.ForeignKey(to='shop.Supplier'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='purchasedetail',
            name='order',
            field=models.ForeignKey(default=None, to='shop.PurchaseOrder'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='purchasedetail',
            name='product',
            field=models.ForeignKey(to='shop.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='product',
            field=models.ForeignKey(to='shop.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='purchase_order',
            field=models.ForeignKey(to='shop.PurchaseOrder'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='sale_order',
            field=models.ForeignKey(default=None, to='shop.SaleOrder', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='company',
            field=models.ForeignKey(to='shop.Supplier'),
            preserve_default=True,
        ),
    ]
