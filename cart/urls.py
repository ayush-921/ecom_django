from django.urls import path

from . import views as cart_views

app_name = 'cart'

urlpatterns = [
    path('', cart_views.cart_summary, name='cart_summary'),
    path('add/', cart_views.cart_add, name='cart_add'),
    path('delete/', cart_views.cart_delete, name='cart_delete'),
    path('update/', cart_views.cart_update, name='cart_update'),
]
