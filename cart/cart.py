from store.models import Product
from decimal import Decimal
from django.core import serializers
"""
general structure of a cart session data which can be obtained when using the get_decoded() method in the shell

{'skey' : {'<productid>' : {'price' : <price>, 'qty' : <qty>}}}

here value of 'skey' is the 'main cart'
eg:
{'skey' : {'1' : {'price' : 399, 'qty' : 4}, '2' : {'price' : 199, 'qty' : 2}}}

cart = {'1' : {'price' : 399, 'qty' : 4}, '2' : {'price' : 199, 'qty' : 2}}
"""

"""
self.cart is original cart
cart is duplicate cart
"""

class Cart():
    """
    This is base class for cart with some default behaviors that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('skey') #if the session has skey then it will be stored in the cart
        if 'skey' not in request.session:
            #if no 'skey' is present in session than the we will create a new dictionary with skey
            cart = self.session['skey'] = {}
        self.cart = cart 

    def add(self, product, product_qty):
        """
        Adding and updating the users basket session data
        """
        qty = product_qty
        product_id = product.id
        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty
        else:
            self.cart[product_id] = {'price': int(product.price), 'qty' : int(product_qty)}

        self.session.modified = True

    def __iter__(self):
        """
        this function is used to collect the product_id in session data to query the database and return products
        We are doing this because in cart_summary page we are sending instance of the this Class as context
        and we need a way to iterate over all the item in the session data
        """
        product_ids = self.cart.keys() #this method collects all the available product id in the cart session data
        # so the cart contains the values for key 'skey' as given the above structure
        # when we say cart.keys() we are asking for keys in the 'main cart' i.e., all the product_id present in cart
        products = Product.products.filter(id__in=product_ids)
        cart = self.cart.copy() #copy of cart data recieved from the session

        for product in products:
            #loop to iterate over all the product in products and add those product detail in the duplicate cart data
            cart[str(product.id)]['product'] = product.id
            cart[str(product.id)]['image'] = product.image.url
            cart[str(product.id)]['productprice'] = product.price
            cart[str(product.id)]['producttitle'] = product.title
            cart[str(product.id)]['producturl'] = product.get_absolute_url()
            """
            after the above duplicate cart wil contain 
            {'1' : {'price' : '399', 'qty' : 4, 'product' : product}}
            """
        for item in cart.values():
            #here when say cart.values() we are iterating over the all the values available for the product_id which is the key in 'main cart'
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['qty']
            #the above line add one more key(i.e., 'total_price') value pair in each of the product_id values 
            """
            after the above cart (i.e., duplicate cart) wil contain 
            {'1' : {'price' : '399', 'qty' : 4, 'product' : product, 'total_price' : 1596}}
            """
            yield item

    def __len__(self):
        """
        Get the cart data and count the qty of items
        """
        return sum(item['qty'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(int(item['price']) * item['qty'] for item in self.cart.values())
    
    def delete(self, productid):
        """
        Delete item from session data
        """
        product_id = str(productid)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True

    def update(self, product, qty):
        """
        update values in session date
        """
        product_id = str(product)
        product_qty = qty

        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty

        self.session.modified = True
