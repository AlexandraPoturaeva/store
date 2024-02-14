from .models import Product, Category, ShoppingCart, ProductInCart
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    ShoppingCartSerializer,
    ManageShoppingCartSerializer,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

header_param = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description="Token {your token}",
    type=openapi.IN_HEADER,
)


class ProductListView(ListAPIView):
    """
    Get a list of all products in the store
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryListView(ListAPIView):
    """
    Get a list of all product categories in the store
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ShoppingCartDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(manual_parameters=[header_param])
    def get(self, request, *args, **kwargs):
        """
        Get the contents of the shopping cart
        """
        shopping_cart = ShoppingCart.objects.filter(user=request.user).first()
        shopping_cart_serializer = ShoppingCartSerializer(shopping_cart)
        return Response(shopping_cart_serializer.data)


class ManageShoppingCartView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(manual_parameters=[header_param])
    def post(self, request):
        """
        Update products in the shopping cart
        (change quantity, add new products)
        """
        payload_serializer = ManageShoppingCartSerializer(data=request.data)
        if not payload_serializer.is_valid():
            return Response(
                data=payload_serializer.errors,
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        products = request.data['products']
        shopping_cart, created = ShoppingCart.objects.get_or_create(
            user=request.user,
        )

        for product in products:
            product_id = product.get('id')
            product_quantity = product.get('quantity')

            try:
                product_obj = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                return Response(
                    data={
                        'id': f'Invalid product id {product_id} - '
                              f'object does not exist',
                    },
                )

            product_in_cart, created = ProductInCart.objects.get_or_create(
                product=product_obj,
                cart=shopping_cart,
            )

            if product_quantity == 0:
                product_in_cart.delete()
            else:
                product_in_cart.quantity = product_quantity
                product_in_cart.save()

        shopping_cart_serializer = ShoppingCartSerializer(shopping_cart)
        return Response(
            shopping_cart_serializer.data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(manual_parameters=[header_param])
    def delete(self, request):
        """
        Clear the shopping cart
        (delete all products from the shopping cart)
        """
        shopping_cart = ShoppingCart.objects.get(user=request.user)
        products_in_cart = ProductInCart.objects.filter(cart=shopping_cart)
        products_in_cart.all().delete()
        shopping_cart_serializer = ShoppingCartSerializer(shopping_cart)
        return Response(
            shopping_cart_serializer.data,
            status=status.HTTP_200_OK,
        )
