from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer
from .models import Product, Category, SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['title']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(
        many=True,
        read_only=True,
        source='subcategory_set',
    )

    class Meta:
        model = Category
        fields = ['title', 'subcategories']


class ProductSerializer(serializers.ModelSerializer):
    cover = VersatileImageFieldSerializer(
        sizes='product_cover',
    )
    category = serializers.CharField(
        read_only=True,
        source='subcategory.category',
    )
    subcategory = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = [
            'title',
            'slug',
            'category',
            'subcategory',
            'price',
            'cover',
        ]
