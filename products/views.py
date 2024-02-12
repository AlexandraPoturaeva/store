from rest_framework.generics import ListAPIView
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
