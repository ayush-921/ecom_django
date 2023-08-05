from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import stripe

@login_required
def CartView(request):
    cart = Cart(request)
    total = str(cart.get_total_price())
    total = total.replace('.', '')
    total = int(total)
    stripe.api_key = "sk_test_51NSxugSCZn81mFB2LG7JYHJ8j9fU0ZNKkb1iwFg276lM2eLy0KIUG2wAJvV1DR0PgnwywcdrtPR8VyNxumZILQw700mpal5oEj"
    
    intent = stripe.PaymentIntent.create(
        amount = total,
        currency='inr',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/home.html', {'client_secret' : intent.client_secret} )
