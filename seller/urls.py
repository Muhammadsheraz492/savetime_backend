
from seller.views import register,login,logout_view,categories,create_gig,packages,gig_details,create_prices,create_description,gigs
from django.urls import path
urlpatterns = [
    
    path("register/",register),
    path("login/",login),
    path("logout/",logout_view),
    path('category/',categories),
    path('activities/',create_gig),
    path('getpackages/',packages),
    path('gigs/',gigs,),
    path('gig_details/<int:id>/',gig_details,),
    path('gig_prices/<int:id>/',create_prices,),
    path('gig_desc/<int:id>/',create_description,)
    
]