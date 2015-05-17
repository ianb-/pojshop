import os, decimal, datetime
from PIL import Image
from easy_thumbnails.files import get_thumbnailer

from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count, Q

from shop.models import *
from forms import *
from blog.models import Article
from helpdesk.models import Ticket

def staff_check(user):
	return user.is_staff

@user_passes_test(staff_check, login_url='/accounts/login/')
def dashboard(request):
	data = {}
	data['sale_count'] = SaleOrder.objects.filter(shipped=False).count()
	data['sales'] = SaleOrder.objects.filter().order_by('-date')[:5]
	data['purchase_count'] = PurchaseOrder.objects.filter(final=False).count()
	data['purchases'] = PurchaseOrder.objects.filter().order_by('-date')[:5]
	data['tickets'] = Ticket.objects.filter().order_by('-datetime')[:5]
	data['ticket_count'] = Ticket.objects.filter(~Q(status="Closed")).count()
	data['viewed'] = Product.objects.all().order_by('-views')[:5]
	data['sold'] = Product.objects.all().order_by('-sales')[:5]
	return render(request, 'cpanel/dashboard.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def products(request):
	data = {}
	try:
		data['products'] = Product.objects.all()
		for p in data['products']:
			p.stock = Item.objects.filter(product=p, is_for_sale=True).count()
	except Product.DoesNotExist:
		data['error'] = 'Some ahs gone wrong! Product not found. Perhaps it never existed!'
	return render(request, 'cpanel/products.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def new_product(request):
	data = {}
	data['categories0'] = Category.objects.filter(level=0)
	data['categories1'] = Category.objects.filter(level=1)
	data['categories2'] = Category.objects.filter(level=2)
	if request.method == 'POST':
		form = ProductForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			p = Product.objects.latest('id')
			for c in request.POST.getlist('category'):
				Product_to_cat.objects.create(product=p,category=Category.objects.get(id=c))
			return redirect('cpanel:product', p.slug)
		else:
			print form.errors
	else:
		form = ProductForm()
	data['form'] = form
	return render(request, 'cpanel/product_new.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def product(request, product_slug):
	if request.method == 'POST':
		img = ProductImage.objects.get(id=request.POST['is_main'])
		if img:
			try:
				main = ProductImage.objects.get(product=img.product, is_main_image=True)
			except ProductImage.DoesNotExist:
				main = None
			if img != main:
				if main:
					main.is_main_image = False
					main.save()
				img.is_main_image = True
				p = img.product
				img.save()
				p.image = img
				p.save()
				return redirect('cpanel:product', img.product.slug)
	data = {}
	try:
		product = Product.objects.get(slug=product_slug)
	except Product.DoesNotExist:
		return HttpResponse("I can't find this product boss")
	data['product'] = product
	data['images'] = ProductImage.objects.filter(product=product).order_by('-is_main_image')
	return render(request, 'cpanel/product.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def new_image(request, product_slug=None):
	if request.method == 'POST':
		try:
			product = Product.objects.get(slug=request.POST['product'])
		except Product.DoesNotExist:
			return redirect('cpanel:new_image', product_slug=product_slug)
		if product:
			pi = ProductImage(product=product, image=request.FILES['image'])
			if request.POST.get('is_main') == 'main_true':
				pi.is_main_image = True
			pi.save()
			if pi.is_main_image:
				product.image = pi
				product.save()
			return redirect('cpanel:product', product.slug)
	if product_slug:
		try:
			product = Product.objects.get(slug=product_slug)
		except Product.DoesNotExist:
			return HttpResponse("I didn't find that product hoss")
	data = {}
	if product:
		data['product'] = product
	else:
		data['products'] = Product.objects.all().order_by('name')
	return render(request, 'cpanel/product_image_new.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def delete_image(request, image_id):
	image = ProductImage.objects.get(id=image_id)
	if image.is_main_image:
		p = image.product
		p.image = None
		p.save()
	product_slug = image.product.slug
	image.delete()
	return redirect('cpanel:product', product_slug)

@user_passes_test(staff_check, login_url='/accounts/login/')
def edit_product(request, product_slug):
	data ={}
	product = Product.objects.get(slug=product_slug)
	data['categories0'] = Category.objects.filter(level=0)
	data['categories1'] = Category.objects.filter(level=1)
	data['categories2'] = Category.objects.filter(level=2)
	p2c = Product_to_cat.objects.filter(product=product)
	data['pcats'] = [x.category for x in p2c]
	form = ProductForm(request.POST, request.FILES or None, instance=product)
	if form.is_valid():
		f = form.save(commit=False)
		if request.POST.get('name'):
			f.slug = slugify(f.name)
			# img_name = 'products/' + f.slug + '.jpg'
			# thumb_name = 'products/' + f.slug + '-thumb.jpg'
			# f.thumbnail = f.image.file
			# f.image.save(img_name,f.image,save=False)
			# f.thumbnail.save(thumb_name,f.thumbnail,save=False)
		f.save()
		for c in request.POST.getlist('category'):
			Product_to_cat.objects.update_or_create(product=product,category=Category.objects.get(id=c))
		# os.remove(old_thumb)
		# os.remove(old_img)
		return redirect('cpanel:products')
	data['product'] = product
	data['form'] = ProductForm()
	return render(request, 'cpanel/product_edit.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def categories(request):
	try:
		categories = Category.objects.all().order_by('level', 'title')
	except Category.DoesNotExist:
		pass
	return render(request, 'cpanel/categories.html', {'categories': categories})

@user_passes_test(staff_check, login_url='/accounts/login/')
def category(request, category_slug):
	try:
		category = Category.objects.get(slug=category_slug)
	except Category.DoesNotExist:
		return HttpResponse("Cannae get this category, cap'n.")
	data = {}
	data['category'] = category
	data['categories'] = Category.objects.all().order_by('level', 'title')
	if request.method == 'POST':
		form = CategoryForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('cpanel:category', category.slug)
		else:
			data['form'] = form
			return render(request, 'cpanel/category.html', data)
	else:
		data['form'] = CategoryForm()
		return render(request, 'cpanel/category.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def new_category(request):
	categories = Category.objects.order_by('title')
	if request.method == 'POST':
		form = CategoryForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('cpanel:categories')
		else:
			print form.errors
	else:
		form = CategoryForm()
	return render(request, 'cpanel/category_new.html', {'form': form, 'categories': categories})

@user_passes_test(staff_check, login_url='/accounts/login/')
def purchases(request):
	data = {}
	data['purchases'] = PurchaseOrder.objects.all().order_by('-date')
	return render(request, 'cpanel/purchases.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def stock(request):
	data = {}
	today = datetime.date.today()
	prev_week = today - datetime.timedelta(days=7)
	prev_month = today - datetime.timedelta(days=28)
	week_sales = Item.objects.filter(sale_order__date__range=(prev_week,today)).values('product__name').annotate(n=Count('product'))
	month_sales = Item.objects.filter(sale_order__date__range=(prev_month,today)).values('product__name').annotate(n=Count('product'))
	products = Product.objects.all()
	data['week'] = week_sales
	data['month'] = month_sales
	data['products'] = products
	return render(request, 'cpanel/stock.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def suppliers(request):
	data = {}
	data['suppliers'] = Supplier.objects.all().order_by('name')
	for supplier in data['suppliers']:
		supplier.contacts = Contact.objects.filter(company=supplier).order_by('firstname')
	return render(request, 'cpanel/suppliers.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def supplier(request, supplier_id):
	supplier = Supplier.objects.get(id=supplier_id)
	if supplier:
		orders = PurchaseOrder.objects.filter(supplier=supplier)
		staff_contacts = Contact.objects.filter(company=supplier)
		data = {'supplier': supplier, 'orders': orders, 'people': staff_contacts}
		return render(request, 'cpanel/supplier.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def new_supplier(request):
	if request.method == 'POST':
		form = SupplierForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(request.META.get('HTTP_REFERER'))
	else:
		form = SupplierForm()
	return render(request, 'cpanel/supplier_new.html', {'form': form})

@user_passes_test(staff_check, login_url='/accounts/login/')
def edit_supplier(request, supplier_id):
	try:
		supplier = Supplier.objects.get(id=supplier_id)
	except Supplier.DoesNotExist:
		return HttpResponse("I couldn't grab that one for you. Send for help.")
	data = {}
	if request.method == 'POST':
		form = SupplierForm(request.POST or None, instance=supplier)
		if form.is_valid():
			form.save()
			return redirect('cpanel:supplier', supplier_id)
		else:
			data['form'] = form
			data['supplier'] = supplier
			return render(request, 'cpanel/supplier_edit.html', data)
	else:
		data['form'] = SupplierForm(instance=supplier)
		data['supplier'] = supplier
		return render(request, 'cpanel/supplier_edit.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')	
def contacts(request):
	data = {}
	data['contacts'] = Contact.objects.all().order_by('lastname')
	data['suppliers'] = Supplier.objects.all().order_by('name')
	return render(request, 'cpanel/contacts.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def new_contact(request):
	data = {}
	data['suppliers'] = Supplier.objects.all().order_by('name')
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			form.save()
			return contacts(request)
		else:
			data['form'] = form
	else:
		data['form'] = ContactForm()
	return render(request, 'cpanel/contact_new.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def edit_contact(request, contact_id):
	data = {}
	try:
		contact = Contact.objects.get(id=contact_id)
	except Contact.DoesNotExist:
		return HttpResponse("Something went wrong. Where's the IT guy?")
	if request.method == 'POST':
		form = ContactForm(request.POST or None, instance=contact)
		if form.is_valid():
			form.save()
			return redirect('cpanel:contacts')
		else:
			data['form'] = form
			data['contact'] = contact
			return render(request, 'cpanel/contact_edit.html', data)
	else:
		data['form'] = ContactForm(instance=contact)
		data['contact'] = contact
		return render(request, 'cpanel/contact_edit.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def purchase(request, purchase_id):
	data = {}
	if request.method == 'POST':
		form = PurchaseDetailForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('cpanel:purchase', purchase_id=purchase_id)
	else:	
		if purchase_id:
			purchase = PurchaseOrder.objects.get(id=purchase_id)
			if purchase:
				purchase_details = PurchaseDetail.objects.filter(order=purchase)
				if purchase.final == False:
					data['remainder'] = purchase.price
					for detail in purchase_details:
						data['remainder'] -= detail.price
					if data['remainder'] == 0:
						purchase.final = True
						purchase.save()
				data['purchase_details'] = purchase_details
				data['purchase'] = purchase
				data['products'] = Product.objects.all().order_by('name')
				data['form'] = PurchaseDetailForm()
		return render(request, 'cpanel/purchase.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def new_purchase(request):
	data = {}
	if request.method == 'POST':
		form = PurchaseOrderForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			purchase = PurchaseOrder.objects.latest('id')
			return redirect('cpanel:purchase', purchase_id=purchase.id)
		else:
			data['form'] = form
	else:
		data['suppliers'] = Supplier.objects.all().order_by('name')

	return render(request, 'cpanel/purchase_new.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def blog(request):
	data = {}
	data['articles'] = Article.objects.all().order_by('-created')
	return render(request, 'cpanel/blog.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def toggle_for_sale(request):
	data = {}
	pid = request.GET['pid']
	product = Product.objects.get(id=pid)
	if product.shelf:
		product.shelf = False
		data['msg'] = 'Removed'
	else:
		product.shelf = True
		data['msg'] = 'Displayed'
	product.save()
	return JsonResponse(data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def sales(request, search=None):
	data = {}
	try:
		search = request.GET['search']
	except:
		search = None
	try:
		sort = request.GET['sort']
	except:
		sort = '-date'
	if search:
		orders = SaleOrder.objects.filter(order_id__icontains=search).order_by(sort)
	else:
		orders = SaleOrder.objects.all().order_by(sort)[:30]
	data['orders'] = orders
	return render(request, 'cpanel/sales.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def shipping(request, order_ref):
	try:
		order = SaleOrder.objects.get(order_id=order_ref)
	except SaleOrder.DoesNotExist:
		return HttpResponse("Error! Order not found yo.")
	if request.method == 'POST':
		if request.POST['tracking']:
			order.tracking_number = request.POST['tracking']
		order.shipped = True
		order.save()
		return redirect('cpanel:shipping', order.order_id)
	products = SaleDetail.objects.filter(order=order)
	items = Item.objects.filter(sale_order=order)
	return render(request, 'cpanel/shipping.html', {'order': order, 'items': items})

@user_passes_test(staff_check, login_url='/accounts/login/')
def invoice(request, order_ref):
	try:
		order = SaleOrder.objects.get(order_id=order_ref)
	except SaleOrder.DoesNotExist:
		return HttpResponse("Error! Order not found yo.")
	data = {}
	data['order'] = order
	data['products'] = SaleDetail.objects.filter(order=order)
	return render(request, 'cpanel/invoice.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def inbox(request):
	data = {}
	data['tickets'] = Ticket.objects.all()
	return render(request, 'cpanel/ticket_inbox.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def item(request, item_id):
	data = {}
	try:
		item = Item.objects.get(id=item_id)
	except Item.DoesNotExist:
		return HttpResponse("Item not found!")
	if request.method == 'POST':
		notes = request.POST['note']
		item.note = notes
		if 'withdraw' in request.POST: #'faulty' checkbox is checked
			if item.sale_order:
				s = item.sale_order
				p = item.product
				item.sale_order = None
				item.sale_price = 0
				try: #replace the item in the sale order
					i = Item.objects.filter(product=p, is_for_sale=True).first()
					i.sale_order = s
					i.sale_price = p.price
					i.save()
				except:
					pass
		item.save()
		return redirect('cpanel:item', item.id)
	data['item'] = item
	data['profit'] = item.sale_price - item.purchase_price
	return render(request, 'cpanel/item.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def report(request, range=None):
	data = {}
	if request.method == 'POST':
		try:
			a = datetime.datetime.strptime(str(request.POST['start_date']), "%m/%d/%Y")
			b = datetime.datetime.strptime(str(request.POST['end_date']), "%m/%d/%Y")
		except:
			b = datetime.today()
			a = datetime.datetime.strptime("01/01/2015", "%d/%m/%Y")
		try:
			purchases = Item.objects.filter(purchase_order__date__range=[a,b])
			sales = Item.objects.filter(sale_order__date__range=[a,b])
		except Item.DoesNotExist:
			return HttpResponse("Something messed up!")
		data['start_date'] = a
		data['end_date'] = b
		data['purchases'] = purchases
		data['sales'] = sales
		out = purchases.aggregate(total=Sum('purchase_price'))
		inc = sales.aggregate(total=Sum('sale_price'))
		data['outgoing_total'] = out['total']
		data['incoming_total'] = inc['total']
		try:
			data['diff'] = inc['total'] - out['total']
		except:
			data['diff'] = 0
	return render(request, 'cpanel/report.html', data)