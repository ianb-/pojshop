# -*- coding: utf-8 -*-
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.files import File
from PIL import Image
from easy_thumbnails.fields import ThumbnailerImageField
import os
from shop.storage import OverwriteStorage

class Supplier(models.Model):
	name = models.CharField(max_length=128)
	address1 = models.CharField(max_length=128)
	address2 = models.CharField(max_length=128, null=True, blank=True)
	city = models.CharField(max_length=128)
	county = models.CharField(max_length=128)
	postcode = models.CharField(max_length=8)
	phone = models.CharField(max_length=12)
	email = models.EmailField(max_length=64)
	notes = models.TextField()

	def __unicode__(self):
		return self.name

class Contact(models.Model):
	company = models.ForeignKey(Supplier)
	title = models.CharField(max_length=24)
	firstname = models.CharField(max_length=32, default=None)
	lastname = models.CharField(max_length=32)
	job_title = models.CharField(max_length=32, blank=True, null=True, default=None)
	phone = models.CharField(max_length=12)
	email = models.EmailField(max_length=64)
	notes = models.TextField()

	def __unicode__(self):
		return unicode(self.firstname + ' ' + self.lastname)

# def upload_filenames(instance, filename):
# 	path = "products/"
# 	filename = '{}.jpg'.format(instance.slug)
# 	return os.path.join(path, filename)

class Category(models.Model):
	title = models.CharField(max_length=24)
	level = models.PositiveSmallIntegerField(default=3)
	parent = models.ForeignKey('Category', null=True, blank=True)
	slug = models.SlugField(unique=True)
	details = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='categories/')
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural = 'Categories'

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Category, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.title

class Product(models.Model):
	name = models.CharField(max_length=64)
	SKU = models.CharField(max_length=64)
	slug = models.SlugField(unique=True)
	details = models.TextField()
	shelf = models.BooleanField(default=False)
	stock = models.PositiveSmallIntegerField(default=0)
	price = models.DecimalField(decimal_places=2, max_digits=6)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	sales = models.IntegerField(default=0)
	image = models.ForeignKey("ProductImage", null=True, blank=True, related_name="cover_photo")

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Product, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name

class ProductImage(models.Model):
	product = models.ForeignKey(Product)
	image = ThumbnailerImageField(upload_to='products')
	is_main_image = models.BooleanField(default=False)

	def __unicode__(self):
		return self.image.name

class Product_to_cat(models.Model):
	product = models.ForeignKey(Product)
	category = models.ForeignKey(Category)

	class Meta:
		verbose_name_plural = 'Product Categorisations'

	def __unicode__(self):
		return str(self.product) + ': ' + str(self.category)

class PurchaseOrder(models.Model):
	supplier = models.ForeignKey(Supplier)
	price = models.DecimalField(max_digits=8,decimal_places=2)
	date = models.DateField()
	final = models.BooleanField(default=False)

	def save(self, *args, **kwargs):
		if self.final:
			items = Item.objects.filter(purchase_order=self)
			details = PurchaseDetail.objects.filter(order=self)
			for item in items:
				item.is_for_sale = True
				item.save()
			for detail in details:
				p = detail.product
				p.shelf = True
				p.stock += detail.quantity
				p.save()
		super(PurchaseOrder, self).save(*args, **kwargs)

	def __unicode__(self):
		return unicode(str(self.date) + ' - ' + self.supplier.name)

class PurchaseDetail(models.Model):
	order = models.ForeignKey(PurchaseOrder, default=None)
	product = models.ForeignKey(Product)
	quantity = models.PositiveSmallIntegerField(default=1)
	price = models.DecimalField(max_digits=6,decimal_places=2)

	def __unicode__(self):
		return unicode(str(self.order) + ': ' + str(self.quantity) + ' x ' + self.product.name)

class SaleOrder(models.Model):
	user = models.ForeignKey(User)
	order_id = models.CharField(max_length=128, unique=True)
	date = models.DateTimeField(auto_now_add=True)
	total_price = models.DecimalField(decimal_places=2, max_digits=8)
	shipping_price = models.DecimalField(decimal_places=2, max_digits=5)
	paid = models.BooleanField(default=False)
	address1 = models.CharField(max_length=128)
	address2 = models.CharField(max_length=128)
	city = models.CharField(max_length=128)
	county = models.CharField(max_length=128)
	postcode = models.CharField(max_length=8)
	phone = models.CharField(max_length=14)
	shipped = models.NullBooleanField(default=False)
	tracking_number = models.CharField(max_length=64, default=None, null=True)
	first_name = models.CharField(max_length=64)
	last_name = models.CharField(max_length=64)

	def __unicode__(self):
		return self.date.strftime('%d, %b %Y') + ' - ' + u'\u00A3' + str(self.total_price) + ' - ' + self.user.username

class SaleDetail(models.Model):
	order = models.ForeignKey(SaleOrder)
	product = models.ForeignKey(Product)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	quantity = models.PositiveSmallIntegerField(default=0)

	def __unicode__(self):
		return self.order.date.strftime('%d, %b %Y') + ': ' + str(self.quantity) + 'x' + self.product.name

	def save(self, *args, **kwargs):
		for i in range(self.quantity):
			item = Item.objects.filter(product=self.product, is_for_sale=True).first()
			item.sale_order = self.order
			item.sale_price = self.product.price
			item.save()
		super(SaleDetail, self).save(*args, **kwargs)

class Item(models.Model):
	product = models.ForeignKey(Product)
	purchase_order = models.ForeignKey(PurchaseOrder)
	sale_order = models.ForeignKey(SaleOrder, null=True, default=None)
	serial = models.CharField(max_length=64, null=True)
	is_for_sale = models.BooleanField(default=False)
	purchase_price = models.DecimalField(decimal_places=2, max_digits=6, default=None)
	sale_price = models.DecimalField(decimal_places=2, max_digits=6, default=None, null=True)
	note = models.TextField(default=None, null=True)

	def save(self, *args, **kwargs):
		p = self.product
		if self.sale_price:
			self.is_for_sale = False
			p.stock -= 1
			p.sales += 1
			p.save()
		if self.is_for_sale:
			p.stock += 1
			p.save()
		super(Item, self).save(*args, **kwargs)

	def __unicode__(self):
		return str(self.id) + ': ' + self.product.name