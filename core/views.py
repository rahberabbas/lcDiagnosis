from django.views.decorators import csrf
from account.models import Profile
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
import random
import string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from .models import Cart, OrderPlaced, PaymentDone
from django.conf import settings
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

def index(request):
    return render(request, 'core/index.html')

from .models import Item
import datetime as dt
import pandas as pd
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
 
def Import_csv(request):
    print('s')               
    try:
        if request.method == 'POST' and request.FILES['myfile']:
          
            myfile = request.FILES['myfile']        
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file) 
            empexceldata = pd.read_csv("."+excel_file,encoding='utf-8')
            print(type(empexceldata))
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():
                obj = Item.objects.create(sid=dbframe.sid,testname=dbframe.testname, testcode=dbframe.testcode,
                                                price=dbframe.price)
                print(type(obj))
                obj.save()
 
            return render(request, 'importexcel.html', {
                'uploaded_file_url': uploaded_file_url
            })    
    except Exception as identifier:            
        print(identifier)
     
    return render(request, 'importexcel.html',{})

def products(request):
    items = Item.objects.all()
    paginator = Paginator(items, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product.html', {
        'items': items,
        'page_obj': page_obj
    })

class ProductDetailView(View):
    def get(self, request, pk):
        product = Item.objects.get(pk=pk)
        return render(request, 'core/detail.html', {'product': product})

@login_required(login_url='/login/')
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Item.objects.get(id=product_id)
    print(user, product)
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required(login_url='/login/')
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        discount_amount = 0.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamt = int((p.product.price))
                amount += tempamt
                total_amount = amount - discount_amount
            return render(request, 'core/order_summary.html', {'cart': cart, 'total': total_amount, 'disc': discount_amount, 'amount': amount})
        else:
            return render(request, 'core/emptycart.html')
    else:
        return redirect('/login')

@login_required(login_url='/login/')
def removecart(request):
    if request.method == "GET":
        product_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=product_id) & Q(user= request.user))
        c.delete()
        amount = 0.0
        discount_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamt = int((p.product.price))
            amount += tempamt
        data = {
            'amount': amount,
            'total': amount - discount_amount
        }
        return JsonResponse(data)

@login_required(login_url='/login/')
def checkout(request):
    user = request.user
    add = Profile.objects.filter(user=user)
    cart_item = Cart.objects.filter(user=user)
    discount_amount = 0.0
    total_amount = 0.0
    amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
    if cart_product:
        for p in cart_product:
            tempamt = int((p.product.price))
            amount += tempamt
        total_amount = amount - discount_amount
        print(total_amount)
        razorpay_amount = total_amount * 100
       
        client = razorpay.Client(auth=("rzp_test_WpP14NdIAkkkGq", "Rk1hqiy74UBrWvlTXG1NW1T9"))
        payment = client.order.create({'amount': total_amount * 100, 'currency': 'INR', 'payment_capture': '1'})
        print(payment)
        PaymentDone(user=request.user, amount=amount, order_id=payment['id']).save()
            # payment_done.save()
    return render(request, 'core/checkout.html', {'add': add, 'total': total_amount, 'razorpay_amount': razorpay_amount ,'cart_item': cart_item})

@csrf_exempt
@login_required(login_url='/login/')
def payment_done(request):
    user = request.user
    customer = Profile.objects.get(user=user)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product= c.product, quantity=1).save()
        c.delete()
    if request.method == "POST":
        a = request.POST
        for key, val in a.items():
            print(val)
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('razorpay_order_id','')
        signature = request.POST.get('razorpay_signature','')
        print(payment_id, order_id, signature)
    return redirect('order')

@csrf_exempt
@login_required(login_url='/login/')
def order(request):

    a = request.POST
    order_id = ""
    for key, val in a.items():
        if key == "razorpay_order_id":
            order_id = val
            break
    pay = PaymentDone.objects.filter(payment_id=order_id).first()
    print(order_id)
    op = OrderPlaced.objects.filter(user=request.user)

    return render(request, 'dashboard/order.html',{'order_placed': op})

def contact(request):
    return render(request, 'core/contact.html')

def about(request):
    return render(request, 'core/about.html')

def service(request):
    return render(request, 'core/service.html')

def covid(request):
    return render(request, 'core/covid.html')