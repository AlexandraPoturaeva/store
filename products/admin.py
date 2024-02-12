from django.contrib import admin
from .models import Product, Category, SubCategory


@admin.register(Product, Category, SubCategory)
class StoreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
