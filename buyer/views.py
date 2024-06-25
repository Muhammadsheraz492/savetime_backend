from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import Buyer_User
from .serializers import BuyerUserSerializer
from django.contrib.auth.hashers import check_password

class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = BuyerUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"success": True, "message": "User registered successfully"}, status=status.HTTP_201_CREATED)
            return Response({"success": False, "message": "Registration failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"success": False, "message": "Registration failed", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
     def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = Buyer_User.objects.get(email=email)
        except Buyer_User.DoesNotExist:
            return Response({'success':False,'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if check_password(password, user.password):
            return Response({'success':True,'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'success':False,'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
