from django.shortcuts import render, HttpResponse
from .models import Product,order, OrderUpdate, Feedback
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum

MERCHANT_KEY = "QkMhaeO8ybGj!2sy"

def index(request):
    allprods = []
    catprods = Product.objects.values('product_cat')
    cats = {item['product_cat'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(product_cat=cat)
        for produc in prod:
            produc.product_amt = int(produc.product_price - (produc.product_discount/100)*produc.product_price)
            produc.save()
        n = len(prod)
        nSlides = n//4 + ceil(n/4 - n//4)
        allprods.append([prod, range(1, nSlides), nSlides])
    params = {'allprods':allprods}
    
    return render(request,'shop/index.html', params)

def searchMatch(query, item):
    if query in item.product_name.lower() or query in item.product_cat.lower() or query in item.product_subcat.lower() or query in item.product_desc.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allprods = []
    catprods = Product.objects.values('product_cat')
    cats = {item['product_cat'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(product_cat=cat)
        prod = [item for item in prodtemp if searchMatch(query.lower(), item)]
        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n//4))
        if len(prod)!=0:
            allprods.append([prod, range(1,nSlides), nSlides])
    params = {'allprods':allprods, 'msg':""}
    if len(allprods) == 0:
        params : {"msg": "0 items found"}
    return render(request, 'shop/search.html', params)          

def about(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phoneno = request.POST.get('phoneno','')
        subject = request.POST.get('subject','')
        msg = request.POST.get('msg','')
        feed = Feedback(name=name, email=email, phoneno=phoneno, subject=subject, msg=msg)
        feed.save();

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
    for prod in product:
        prod.product_amt = int(prod.product_price - (prod.product_discount/100)*prod.product_price)
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
        amount = request.POST.get("amount",0)
        ord = order(items_json=items_json ,name=name, email=email, address=address, city=city, state=state, zipcode=zipcode, phone=phone, amount=amount)
        ord.save()
        thank = True
        id = ord.order_id
        ordupdate = OrderUpdate(order_id = id, update_desc="The order has been placed")
        ordupdate.save()
        param_dict = {
            'MID':'CGTtuV46964642507305',
            'ORDER_ID': str(ord.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
	        'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        #return render(request, 'shop/checkout.html',{'id':id, 'thank':thank})
        return render(request, 'shop/paytm.html', {'param_dict':param_dict})

    return render(request,'shop/checkout.html');

@csrf_exempt
def handlerequest(request):
    form = request.POST
    resp_dict = {}
    for i in form.keys():
        resp_dict[i] = form[i]
        if(i == 'CHECKSUMHASH'):
            checksum = form[i]

    verify = Checksum.verify_checksum(resp_dict, MERCHANT_KEY, checksum)
    if not verify:
        print("Payment Tampering")
        return HttpResponse("Dont try to act smart, someone's watching")
    else:
        return render(request, 'shop/paymentstatus.html', {'response':resp_dict})