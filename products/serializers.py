from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer
from .models import Product, Category, SubCategory, ShoppingCart, ProductInCart


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
            'id',
            'title',
            'slug',
            'category',
            'subcategory',
            'price',
            'cover',
        ]


class ProductInCartSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    price_for_one = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = ProductInCart
        fields = ['id', 'title', 'quantity', 'price_for_one']

    def get_id(self, obj):
        return obj.product.id

    def get_title(self, obj):
        return obj.product.title

    def get_price_for_one(self, obj):
        return obj.product.price

    def get_quantity(self, obj):
        return obj.quantity


class ShoppingCartSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = ['products', 'total_price']

    def get_products(self, obj):
        products = ProductInCart.objects.filter(
            cart=obj,
        ).prefetch_related('product')
        return [ProductInCartSerializer(product).data for product in products]

    def get_total_price(self, obj):
        products = ProductInCart.objects.filter(
            cart=obj,
        ).prefetch_related('product')

        total_price = sum([
            product.product.price * product.quantity
            for product in products
        ])
        return total_price


class UpdateProductInCartSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=0)


class ManageShoppingCartSerializer(serializers.Serializer):
    products = UpdateProductInCartSerializer(many=True)
