from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from models import Category, Product, ProductImage, Product_to_cat, Item, SaleOrder, SaleDetail
from forms import SaleOrderForm
from helpdesk.models import Ticket
from django.contrib.auth.decorators import login_required
import random

def menu(category_slug=None):
    data = {}
    data['categories'] = Category.objects.filter(level=0).order_by('-views')
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            data['error'] = "This isn't a valid category"
        data['category'] = category
        data['parent'] = category.parent
        data['siblings'] = Category.objects.filter(parent=category.parent).order_by('-views')
        data['children'] = Category.objects.filter(parent=category).order_by('-views')
    return data

def front(request):
    data = menu()
    products = Product.objects.filter(shelf=True)[:12]
    data['products'] = products
    return render(request, 'shop/frontpage.html', data)

def category(request, category_slug, pg=None):
    per_page = 1 #products per page!
    if pg:
        pg = int(pg)
    else:
        pg = 1
    context = menu(category_slug)
    category = context['category']
    if category:
        p2c = Product_to_cat.objects.filter(category=category).filter(product__shelf=True)
        products = [p.product for p in p2c]
        n = len(products)
        context['products'] = products[(pg*per_page)-per_page:pg*per_page]
        context['page'] = {
            'this': pg,
            'previous': pg-1,
            'next': pg+1,
            'pages': range(1,divmod(n,per_page)[0]+1)
            }
        category.views += 1
        category.save()
    return render(request, 'shop/category.html', context)

def product(request, product_slug):
    context = {}
    try:
        product = Product.objects.get(slug=product_slug)
    except Product.DoesNotExist:
        return HttpResponse("This isn't a valid product")
    if product:
        p2c = Product_to_cat.objects.filter(product=product).order_by('-category').first()
        context = menu(p2c.category.slug)
        context['product'] = product
        context['image'] = ProductImage.objects.get(product=product, is_main_image=True)
        context['images'] = ProductImage.objects.filter(product=product, is_main_image=False)
        context['stock'] = Item.objects.filter(product=product).count()
        product.views += 1
        product.save()
    return render(request, 'shop/product.html', context)

def trolley(request):
    data = {}
    products = {}
    trolley = request.session.get('trolley')
    data['categories'] = Category.objects.filter(level=0).order_by('-views')
    if trolley:
        data['products'] = Product.objects.filter(id__in=trolley['contents'].keys())
        data['trolley'] = trolley
    return render(request, 'shop/trolley.html', data)

def add_to_trolley(request):
    trolley = request.session.get('trolley')
    if not trolley:
        trolley = {
            'meta': {
                'amount': 0,
                'total': 0,
            },
            'contents': {
            }
        }

    if request.method == 'GET':
        product_id = request.GET['product_id']

    if product_id:
        product = Product.objects.get(id=product_id)
        if product:
            if product.stock == 0:
                trolley['meta']['message'] = 'Out of stock'
                return JsonResponse(trolley)
            total = float(trolley['meta']['total'])
            if product_id in trolley['contents']:
                qty = trolley['contents'][product_id]['quantity']
                if product.stock <= qty:
                    trolley['meta']['message'] = 'Only ' + str(product.stock) + ' remaining!'
                    return JsonResponse(trolley)
                trolley['contents'][product_id]['quantity'] = qty + 1
                trolley['meta']['total'] = total + float(product.price)
            else:
                trolley['contents'][product_id] = {
                    'p_name': product.name,
                    'slug': product.slug,
                    'quantity': 1,
                    'price': str(product.price),
                    }
                trolley['meta']['amount'] = len(trolley['contents'])
                trolley['meta']['total'] = total + float(product.price)
            trolley['meta']['message'] = 'Added!'
            request.session['trolley'] = trolley

    return JsonResponse(trolley)

def remove_from_trolley(request):
    trolley = request.session.get('trolley')
    if trolley:
        if request.method == 'GET':
            product_id = request.GET['product_id']
            n_to_remove = request.GET['quantity']
        if product_id:
            product = Product.objects.get(id=product_id)
            if product:
                total = 0
                if n_to_remove == "all":
                    del trolley['contents'][product_id]
                else:
                    t_qty = trolley['contents'][product_id]['quantity']
                    t_qty -= int(n_to_remove)
                    print 't_qty: ' + str(t_qty)
                    if t_qty > 0:
                        trolley['contents'][product_id]['quantity'] = t_qty
                    else:
                        del trolley['contents'][product_id]
                for key, value in trolley['contents'].items():
                    total += value['quantity'] * float(value['price'])
                trolley['meta']['total'] = total
                trolley['meta']['amount'] = len(trolley['contents'])
                request.session['trolley'] = trolley
        return JsonResponse(trolley)
    return HttpResponse('empty')

def empty_trolley(request):
    request.session['trolley'] = None
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def checkout(request):
    data = {}
    trolley = request.session.get('trolley')
    if trolley == None:
        return HttpResponse("Your trolley is empty. There's nothing to check out!")
    order = SaleOrder.objects.filter(user=request.user, paid=False).first()
    if order:
        data['order'] = order
        if order.total_price == float("{0:.2f}".format(trolley['meta']['total'])):
            return render(request, 'shop/order.html', data)
        else:
            return render(request, 'shop/delivery.html', data)
    else:
        if request.method == 'POST':
            form = SaleOrderForm(request.POST)
            if form.is_valid():
                of = form.save(commit=False)
                of.user = request.user
                while True:
                    oid = str(random.randint(999,9999)) + '-' + str(random.randint(999,9999)) + '-' + str(random.randint(999,9999))
                    try:
                        o = SaleOrder.objects.get(order_id=oid)
                    except SaleOrder.DoesNotExist:
                        break
                of.order_id = oid
                of.total_price = trolley['meta']['total']
                of.shipping_price = 3.99
                of.paid = True
                of.save()
                for p in trolley['contents']:
                    n = trolley['contents'][p]['quantity']
                    product = Product.objects.get(id=p)
                    order = SaleOrder.objects.get(order_id=oid)
                    price = float(trolley['contents'][p]['price']) * n
                    sale = SaleDetail(order=order, product=product, price=price, quantity=n)
                    sale.save()
                request.session['trolley'] = None
                return redirect('shop:history')
            else:
                data['form'] = form
                return render(request, 'shop/delivery.html', data)
        else:
            trolley = request.session.get('trolley')
            form = SaleOrderForm()
            data['form'] = form
        return render(request, 'shop/delivery.html', data)

@login_required
def history(request):
    data = {}
    data['orders'] = SaleOrder.objects.filter(user=request.user).order_by('-date')
    data['tickets'] = Ticket.objects.filter(user=request.user)
    data['user'] = request.user
    return render(request, 'shop/history.html', data)

@login_required
def order(request, order_id):
    try:
        order = SaleOrder.objects.get(order_id=order_id, user=request.user)
    except SaleOrder.DoesNotExist:
        return HttpResponse('There has been some kind of mistake.')
    data = {}
    data['order'] = order
    data['items'] = SaleDetail.objects.filter(order=order)
    return render(request, 'shop/order.html', data)