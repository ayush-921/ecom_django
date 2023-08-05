from django.urls import path
from . import views
from .views import StripeIntentView
app_name = 'usercart'

urlpatterns = [
    path('', views.usercart_summary, name='usercart_summary'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('create-payment-intent/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('success/', views.success, name="success"),
    path('webhooks/stripe/', views.stripe_webhook, name="stripe_webhook")
]
