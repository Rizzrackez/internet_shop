from django.shortcuts import render, redirect
from ecomapp.models import Category, Product, Cart, CartItem, Order
from django.http import JsonResponse
from decimal import Decimal
from ecomapp.forms import OrderForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from ecomapp import urls
from django.contrib.auth.views import LoginView


def home_page(request):
    categories = Category.objects.all()
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product = Product.objects.all().filter(available=True)
    context = {
        'cart' : cart,
        'categories': categories,
        'product': product
    }
    return render(request, 'ecomapp/home.html', context)


def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    categories = Category.objects.all()
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    context = {
        'product': product,
        'categories': categories,
        'cart': cart,
    }
    return render(request, 'ecomapp/product_detail.html', context)


def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    products_on_category = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products_on_category': products_on_category
    }
    return render(request, 'ecomapp/category_detail.html', context)


def view_cart(request):
    product = Product.objects.all().filter(available=True)
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    context = {
        'cart': cart,
        'product': product,

    }
    return render(request, 'ecomapp/cart.html', context)


def add_to_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    slug = request.GET.get('slug')
    product = Product.objects.get(slug=slug)
    cart.add_to_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


def remove_from_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    slug = request.GET.get('slug')
    product = Product.objects.get(slug=slug)
    cart.remove_from_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total} )


def change_item_qty(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart_item = CartItem.objects.get(id=int(item_id))
    cart_item.qty = int(qty)
    cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
    cart_item.save()
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.items.count(),
                         'item_total': cart_item.item_total,
                         'cart_total_price': cart.cart_total})


def checkout_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    context = {
        'cart': cart
    }
    return render(request, 'ecomapp/checkout.html', context)


def order_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            buying_type = form.cleaned_data['buying_type']
            address = form.cleaned_data['address']
            comments = form.cleaned_data['comments']
            new_order = Order()
            new_order.save()
            new_order.items.add(cart)
            new_order.first_name = name
            new_order.last_name = last_name
            new_order.phone = phone
            new_order.address = address
            new_order.buying_type = buying_type
            new_order.comments = comments
            new_order.total = cart.cart_total
            new_order.save()
            del request.session['cart_id']
            del request.session['total']
            return redirect('home')
    else:
        form = OrderForm()
    return render(request, 'ecomapp/order.html', {'form': form})

