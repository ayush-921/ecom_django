from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserEditForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .tokens import account_activation_token
from .models import UserBase
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse

#cart cookie import
from cart.cart import Cart
from usercart.models import *
from store.models import Product
# Create your views here.


@login_required
def dashboard(request):
    return render(request, "account/user/dashboard.html")


@login_required
def edit_details(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, "account/user/edit_details.html", {"user_form": user_form})


@login_required
def delete_user(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect("account:delete_confirmation")

def sign_in(request):
    if request.method == "POST":
        loginForm = UserLoginForm(request.POST)
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                cart = Cart(request)
                order, created = Order.objects.get_or_create(customer=user, complete=False)
                
                
                for cartItem in cart:
                    print(cartItem)
                    prod = Product.objects.filter(pk=cartItem['product']).first()
                    print(prod)
                    if OrderItem.objects.filter(order=order).filter(product=prod).exists():
                        item = OrderItem.objects.filter(order=order).filter(product=prod).first()
                        print(item)
                        item.quantity = item.quantity + cartItem['qty']
                        item.save()
                    else:
                        OrderItem.objects.create(
                            product=prod,
                            order=order,
                            quantity=cartItem['qty'],
                        )
                login(request, user)
                return redirect("account:dashboard")
        else:
            print("form invalid ")
    else:
        print("get method")
        loginForm = UserLoginForm()
        return render(request, "account/registration/login.html", {'loginForm' : loginForm})

    return render(request, "account/registration/login.html", {'loginForm' : loginForm})

def account_register(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()

            # setup email
            current_site = get_current_site(request)
            subject = "Activate your account"
            message = render_to_string(
                "account/registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            return HttpResponse("registered succesfully and activation sent")
    else:
        registerForm = RegistrationForm()

    return render(request, "account/registration/register.html", {"form": registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except:
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("account:dashboard")
    else:
        return (request, "account/registration/activation_invalid.html")
