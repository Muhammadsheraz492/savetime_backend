from seller.views import register,login,logout_view
from django.urls import path
from .views import *
urlpatterns = [
    path("login/", post_login, name='login'),  
    path("user/", AdminUserAPIView.as_view(), name='admin-user-list'),  
    path("category/", post_category, name='category'),
      

]
