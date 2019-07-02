from django.shortcuts import render, HttpResponse
from .models import Product
from math import ceil

def index(request):
    allprods = []
    catprods = Product.objects.values('product_cat')
    cats = {item['product_cat'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(product_cat=cat)
        for produc in prod:
            produc.product_amt = int(produc.product_price - (produc.product_discount/100)*produc.product_price)
        n = len(prod)
        nSlides = n//4 + ceil(n/4 - n//4)
        allprods.append([prod, range(1, nSlides), nSlides])
    params = {'allprods':allprods}
    
    return render(request,'shop/index.html', params)

def about(request):
    return render(request,'shop/about.html')

def track(request):
    return render(request,'shop/tracker.html')

def productview(request, id):
    product = Product.objects.filter(id=id)
    print(product)
    return render(request,'shop/viewproduct.html',{'product':product[0]})