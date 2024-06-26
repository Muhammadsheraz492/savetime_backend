from django.urls import path
from .views import RegisterView, LoginView,OrderView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('order/',OrderView.as_view(),name='order')   
]
