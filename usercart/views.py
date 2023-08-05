from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from core import settings
from .models import *
from django.http import HttpResponse, JsonResponse
import json
import datetime
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.


def usercart_items(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    context = {"cartItems": cartItems}
    return context


def usercart_summary(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "usercart/summary.html", context)

@login_required
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        items = []
        cartItems = order["get_cart_items"]

    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, "usercart/checkout.html", context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]

    print("Action: ", action)
    print("productId: ", productId)

    customer = request.user
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1

    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data["form"]["total"])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True

        order.save()

        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data["shipping"]["address"],
            city=data["shipping"]["city"],
            state=data["shipping"]["state"],
            zipcode=data["shipping"]["zipcode"],
        )

    else:
        print("User not logged in...")
    return JsonResponse("Payment Complete", safe=False)


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user = UserBase.objects.filter(pk=data["user_id"]).first()
            order = Order.objects.filter(pk=data["order_id"]).first()
            price = order.get_cart_total
            price = price * 100
            intent = stripe.PaymentIntent.create(
                amount=price,
                currency="inr",
                automatic_payment_methods={
                    "enabled": True,
                },
                metadata={
                    'address' : data['address'],
                    'city' : data['city'],
                    'state' : data['state'],
                    'zipcode' : data['zipcode'],
                    'order_id' : data['order_id'],
                    'user_id' : data['user_id'],
                },
            )

            return JsonResponse({"clientSecret": intent["client_secret"]}, safe=False)
        except Exception as e:
            return JsonResponse(
                {
                    "error": str(e),
                }
            )


def success(request):
    return render(request, "usercart/success.html")


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'payment_intent.succeeded':
        intent = event["data"]["object"]
        user_id = intent['metadata']['user_id']
        order_id = intent['metadata']['order_id']
        transaction_id = datetime.datetime.now().timestamp()
        user = UserBase.objects.filter(pk=user_id).first()
        order = Order.objects.filter(pk=order_id).first()
        order.complete = True
        order.transaction_id = transaction_id
        order.save()

        ShippingAddress.objects.create(
            customer=user,
            order=order,
            address=intent["metadata"]["address"],
            city=intent["metadata"]["city"],
            state=intent["metadata"]["state"],
            zipcode=intent["metadata"]["zipcode"],
        )
    
    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)
