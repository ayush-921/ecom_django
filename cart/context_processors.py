#context processors include those views which should be available all the website without using the url
from .cart import Cart

def cart(request):
    return {'cart' : Cart(request)}