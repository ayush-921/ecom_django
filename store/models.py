from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class ProductManager(models.Manager):
    #Product manager is custom object manager which only takes those products which are active
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)

class Category(models.Model):
    name = models.CharField(
        max_length=255, db_index=True
    )  # db_index is used for faster lookup when values are unique in column
    slug = models.SlugField(
        max_length=255, unique=True
    )  # slug field is entered in url to access the particular page

    class Meta:
        verbose_name_plural = "catergories"

    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="profuct", on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="product_creator"
    )
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default="admin")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="images/")
    slug = models.SlugField(max_length=255)
    price = models.IntegerField()
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager() #default object manager
    products = ProductManager() #custome manager only taking is_active element in queryset

    class Meta:
        verbose_name_plural = "Products"
        ordering = ("-created",)

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])
    

    def __str__(self):
        return self.title
