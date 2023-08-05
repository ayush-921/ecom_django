from django.contrib import admin
from .models import Category, Product

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
    ]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # this class maintains how the Product objects will be visible in the admin page
    list_display = [
        "title",
        "author",
        "slug",
        "price",
        "in_stock",
        "created",
        "updated",
    ]  # this columns will be visible for each of the products
    list_filter = ["in_stock", "is_active"]  # need to read first
    list_editable = [
        "price",
        "in_stock",
    ]  # in the products table in admin this two fields are editable
    prepopulated_fields = {
        "slug": ("title",)
    }  # slug will be autofilled with whatever the text present in tilte field
