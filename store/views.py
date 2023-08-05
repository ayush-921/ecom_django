from django.shortcuts import render, get_object_or_404
from .models import Category, Product

# Create your views here.

def categories(request):
    #this view is added to context_processors in templates page of all the view so that is available in all the pages
    return {
        'categories' : Category.objects.all()
    }

def all_products(request):
    products = Product.products.all() #.products. is the custom product manager only taking active products into consideration
    return render(request, "store/home.html", {"products": products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/products/detail.html', {'product' : product})

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug = category_slug) #used to find the name of the category
    products = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html', {'category': category, 'products': products})  