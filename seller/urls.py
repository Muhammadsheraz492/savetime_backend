
from seller.views import register,login,logout_view
from django.urls import path
urlpatterns = [
    
    path("register/",register),
    path("login/",login),
    path("logout/",logout_view)
    
    
]