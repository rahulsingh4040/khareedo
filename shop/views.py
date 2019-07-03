from django.shortcuts import render, HttpResponse
from .models import Product,order, OrderUpdate
from math import ceil
import json

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
    if request.method == 'POST':
        order_id = request.POST.get('order_id', '')
        email = request.POST.get('email','')
        try:
            ord = order.objects.filter(order_id=order_id, email=email)
            if len(ord)>0:
                update = OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc, 'time':item.timestamp})
                    response = json.dumps([updates, ord[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
            
    return render(request,'shop/tracker.html')

def productview(request, id):
    product = Product.objects.filter(id=id)
    print(product)
    return render(request,'shop/viewproduct.html',{'product':product[0]})

def checkout(request):
    if request.method == "POST":
        name = request.POST.get("name",'')
        email = request.POST.get("email",'')
        address = request.POST.get("address1",'') + " " + request.POST.get("address2", '')
        city = request.POST.get("city",'')
        state = request.POST.get("state",'')
        zipcode = request.POST.get("zip",'')
        phone = request.POST.get("contact",'')
        items_json = request.POST.get("itemsJson", '')
        ord = order(items_json=items_json ,name=name, email=email, address=address, city=city, state=state, zipcode=zipcode, phone=phone)
        ord.save()
        thank = True
        id = ord.order_id
        ordupdate = OrderUpdate(order_id = id, update_desc="The order has been placed")
        ordupdate.save()
        return render(request, 'shop/checkout.html',{'id':id, 'thank':thank})

    return render(request,'shop/checkout.html');