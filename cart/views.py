from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
import json
# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    print(cart)
    return render(request, 'cart/summary.html', {'cart' : cart})

def cart_add(request):
    cart = Cart(request) #creates a cart object which contains session request data
    if request.POST.get('action') == 'post':
        #makes sure that the request we got from ajax is post request
        product_id = int((request.POST.get('productid')))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        
        cart.add(product=product, product_qty=product_qty)
        
        cart_total_qty = cart.__len__()
        response = JsonResponse({'qty':cart_total_qty,})
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        productid = int(request.POST.get('productid'))
        cart.delete(productid=productid)

        cartqty = cart.__len__()
        carttotal = cart.get_total_price()

        response = JsonResponse({'Success': True, 'qty': cartqty, 'totalprice' : carttotal})

        return response
    
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product_price = int(float(request.POST.get('productprice')))
        
        cart.update(product=product_id, qty=product_qty)
        
        product_total_price = str(product_qty*product_price)

        cartqty = cart.__len__()
        carttotal = cart.get_total_price()

        response = JsonResponse({'Success': True, 'prodtotprice': product_total_price, 'qty': cartqty, 'totalprice' : carttotal})
        return response