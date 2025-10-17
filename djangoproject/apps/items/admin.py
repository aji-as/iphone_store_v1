from django.contrib import admin

# Register your models here.
from apps.items .models import Product

admin.site.register(Product)
