from django.urls import path
from .views import (
    ProductListView,
    CategoryListView,
    ShoppingCartDetailView,
    ManageShoppingCartView,
)

urlpatterns = [
    path('products/', ProductListView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path('shopping-cart/', ShoppingCartDetailView.as_view()),
    path('shopping-cart/manage/', ManageShoppingCartView.as_view()),
]
