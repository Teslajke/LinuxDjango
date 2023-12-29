from django.shortcuts import render


def shop_index(request):
    return render(request, 'shopapp/shop-index.html')
