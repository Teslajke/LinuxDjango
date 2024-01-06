from timeit import default_timer
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import Group

from .models import Product, Order


def shop_index(request: HttpRequest):
    products = [
        ('laptop', 1999),
        ('desktop', 2999),
        ('smartphone', 999),
    ]
    context = {
        'time_running': default_timer(),
        'products': products,
    }
    return render(request, 'shopapp/shop-index.html', context=context)


def groups_list(request: HttpRequest):
    context = {
        # we also load connected with Group property 'permissions' to run it faster
        'groups': Group.objects.prefetch_related('permissions').all(),
    }
    return render(request, 'shopapp/groups-list.html', context=context)


def products_list(request: HttpRequest):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'shopapp/products-list.html', context=context)


def orders_list(request: HttpRequest):
    context = {
        #  select_related - will also load all related users to run faster
        'orders': Order.objects.select_related('user').prefetch_related('products').all()
    }
    return render(request, 'shopapp/orders-list.html', context=context)
