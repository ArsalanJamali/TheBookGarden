from django.shortcuts import render
from django.views.generic import TemplateView
from customer_app.models import AddressBook
import json
from thebookgarden.utils import get_new_cart_items_subtotal
from django.http import JsonResponse
from django.core import serializers
from django.http import Http404
from .models import Order,OrderItem
from django.contrib.auth import get_user_model
from product_app.models import Book

# Create your views here.

def create_order_item_instances(cart,order_obj):
    for key,qty in cart.items():
        key=int(key)
        qty=int(qty)
        book_obj=None
        try:
            book_obj=Book.objects.get(pk=key)
        except:
            book_obj=None
        if book_obj!=None:    
            orderitem_obj=OrderItem(order=order_obj,book=book_obj,quantity=qty,short_book_info=None)
            orderitem_obj.save()




def CheckoutOrderView(request):
    if request.method == 'POST':
        bfname=request.POST['first_name_bill']
        blname=request.POST['last_name_bill']
        bemail=request.POST['email_bill']
        bcountry=request.POST['country_bill']
        baddress=request.POST['address_bill']
        bcity=request.POST['city_bill']
        bzipcode=request.POST['zipcode_bill']
        bphone=request.POST['phone_number_bill']
        comment=request.POST['comment']
        checkbox=request.POST.get('ship_different',False)
        shipping_address=''
        billing_address=''
        sfname=bfname
        slname=blname
        semail=bemail
        sphone=bphone
        scountry=bcountry
        saddress=baddress
        scity=bcity
        szipcode=bzipcode
        if type(checkbox) == type('on') and checkbox=='on':
            sfname=request.POST['first_name_ship']
            slname=request.POST['last_name_ship']
            semail=request.POST['email_ship']
            scountry=request.POST['country_ship']
            saddress=request.POST['address_ship']
            scity=request.POST['city_ship']
            szipcode=request.POST['zipcode_ship']
            sphone=request.POST['phone_number_ship']

        billing_address=baddress+','+bcity+','
        if bzipcode == '':
            billing_address+=bcountry
        else:
            billing_address+=(bzipcode+','+bcountry)    

        shipping_address=saddress+','+scity+','
        if szipcode == '':
            shipping_address+=scountry
        else:
            shipping_address+=(szipcode+','+scountry)

        cart=None
        try:
            cart=request.COOKIES['cart']
        except:
            cart=None
        if cart==None or len(json.loads(cart))==0:
            raise Http404()
        else:
            user=None
            if request.user.is_authenticated:
                user=request.user
            order_obj=Order(billing_first_name=bfname,billing_last_name=blname,billing_email=bemail,
                            billing_address=billing_address,billing_phone_number=bphone,
                            shipping_first_name=sfname,shipping_last_name=slname,shipping_email=semail,
                            shipping_address=shipping_address,shipping_phone_number=sphone,
                            customer=user,order_status=1,payment_status=0,order_guideline=comment
                            )
            order_obj.save()
            create_order_item_instances(json.loads(cart),order_obj)
            response=render(request,'index.html')
            response.delete_cookie('cart')
            return response                    
    else:
        context={}
        if request.user.is_authenticated:
            context['saved_address']=AddressBook.objects.filter(user=request.user).order_by('-is_default','-pk')
            if context['saved_address'].count()==0:
                context['no_address']=True
            else:
                context['no_address']=False

        cart=None
        try:    
            cart=request.COOKIES['cart']
        except:
            cart=None

        if cart==None or len(json.loads(cart))==0:
            context['is_empty']=True
            context['subtotal']=0
            context['tax']=0
            context['total']=0             
        else:
            context['is_empty']=False
            cart=json.loads(cart)
            _,context['subtotal']=get_new_cart_items_subtotal(cart)
            context['tax']=round(context['subtotal']*0.13,2)
            context['total']=round(context['subtotal']+context['tax'],2)
        return render(request,'checkout.html',context)
            


def getAddressObject(request):
    if request.is_ajax():
        address_pk=int(request.GET.get('id'))
        returned_dic= serializers.serialize('json',AddressBook.objects.filter(pk=address_pk))
        return JsonResponse(returned_dic,status=200,safe=False)







    