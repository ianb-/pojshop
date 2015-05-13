from django import forms
from shop.models import Category, Product, Supplier, Contact, PurchaseOrder, PurchaseDetail, Item
from django.template.defaultfilters import slugify
from django.core.validators import RegexValidator
from PIL import Image
from easy_thumbnails.files import get_thumbnailer
import os

class CategoryForm(forms.ModelForm):
    title = forms.CharField(max_length=64)
    details = forms.CharField(widget=forms.Textarea(), required=False)
    image = forms.ImageField()
    level = forms.CharField()
    parent = forms.CharField()

    class Meta:
        model = Category
        fields = ('title','details','image','level',)

class ProductForm(forms.ModelForm):
	name = forms.CharField(max_length=64)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)
	SKU = forms.CharField(max_length=64)
	details = forms.CharField(widget=forms.Textarea())
	price = forms.DecimalField(min_value=0)

	class Meta:
		model = Product
		fields = ('name','SKU','price','details','slug')

class SupplierForm(forms.ModelForm):
	name = forms.CharField(max_length=128)
	address1 = forms.CharField(max_length=128)
	address2 = forms.CharField(max_length=128, required=False)
	city = forms.CharField(max_length=32)
	county = forms.CharField(max_length=32)
	postcode = forms.CharField(max_length=8)
	phone = forms.CharField(validators=[
		RegexValidator(
			regex='(0|44)(\d{4}\s(\d{6}|\d{3}\s\d{3})|\d{10})',
			message="Please ensure you're entering a valid UK telephone number"),
		])
	email = forms.EmailField(max_length=128)
	notes = forms.CharField(widget=forms.Textarea())

	class Meta:
		model = Supplier
		fields = ('name', 'address1', 'address2', 'city', 'county', 'postcode', 'phone', 'email', 'notes')

class ContactForm(forms.ModelForm):
	company = forms.CharField()
	title = forms.CharField(max_length=24)
	firstname = forms.CharField(max_length=32)
	lastname = forms.CharField(max_length=32, required=False)
	job_title = forms.CharField(max_length=32)
	phone = forms.CharField(required=False, validators=[
		RegexValidator(
			regex='(0|44)(\d{4}\s(\d{6}|\d{3}\s\d{3})|\d{10})',
			message="Please ensure you're entering a valid UK telephone number"),
		])
	email = forms.EmailField(max_length=64)
	notes = forms.CharField(widget=forms.Textarea())

	class Meta:
		model = Contact
		fields = ('company', 'title', 'firstname', 'lastname', 'job_title', 'phone', 'email', 'notes')

	def clean_company(self):
		supplier = self.cleaned_data.get('company')
		company = Supplier.objects.get(id=int(supplier))
		return company

class PurchaseOrderForm(forms.ModelForm):
	supplier = forms.CharField()
	price = forms.DecimalField(min_value=0, decimal_places=2)
	date = forms.DateField()

	class Meta:
		model = PurchaseOrder
		exclude = ['final',]

	def clean_supplier(self):
		supplier = self.cleaned_data.get('supplier')
		supplier = Supplier.objects.get(id=int(supplier))
		return supplier

class PurchaseDetailForm(forms.ModelForm):
	product = forms.CharField()
	quantity = forms.CharField()
	price = forms.DecimalField(min_value=0, decimal_places=2)
	order = forms.CharField(widget=forms.HiddenInput())

	class Meta:
		model = PurchaseDetail
		fields = ['quantity', 'price', 'order', 'product']

	def clean_product(self):
		product = self.cleaned_data.get('product')
		product = Product.objects.get(id=int(product))
		order = self.cleaned_data.get('order')
		#order = PurchaseOrder.objects.get(id=int(order))
		quantity = int(self.cleaned_data.get('quantity'))
		price = float(self.cleaned_data.get('price'))
		ppu = price / quantity
		for n in range(quantity):
			i = Item(product=product, purchase_order=order, serial=None, purchase_price=ppu, sale_price=None)
			i.save()
		return product

	def clean_order(self):
		order = self.cleaned_data.get('order')
		order = PurchaseOrder.objects.get(id=int(order))
		return order