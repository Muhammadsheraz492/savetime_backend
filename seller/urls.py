
from seller.views import register,login,logout_view,categories
from django.urls import path
urlpatterns = [
    
    path("register/",register),
    path("login/",login),
    path("logout/",logout_view),
    path('category/',categories) 
]