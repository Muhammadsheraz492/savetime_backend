from seller.views import register,login,logout_view
from django.urls import path
from .views import *
urlpatterns = [
    path("login/", post_login, name='login'),  # URL pattern for login endpoint
    path("user/", AdminUserAPIView.as_view(), name='admin-user-list'),  # URL pattern for AdminUserAPIView
]
