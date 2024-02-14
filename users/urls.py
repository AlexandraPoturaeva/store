from django.urls import path
from users.views import UserRegistrationView
from rest_framework.authtoken import views


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='registration'),
    path('auth/', views.obtain_auth_token, name='authentication'),
]
