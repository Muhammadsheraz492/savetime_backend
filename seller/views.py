from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user_agents import parse
from .serializers import SellerSerializer,LoginSerializer
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from rest_framework.authtoken.models import Token
import traceback
from rest_framework.authentication import TokenAuthentication
import jwt,datetime
from .models import *
from .serializers import LoginSerializer
from seller import serializers
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from common.models.category import Category
from common.serializer.category_serialzer import CategorySerializer
def serialize_errors(errors):
    serialized_errors = []
    for field, messages in errors.items():
        for message in messages:
            serialized_errors.append({field: str(message)})
    return serialized_errors
def serialize_exception(exception):
    return {
        'type': type(exception).__name__,
        'message': serialize_errors(exception.detail),
    }
@api_view(['POST'])
def register(request):
    try:
        data = request.data.copy()
        print(data)
        # input("Hello Testing")
        serializer = SellerSerializer(data=data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # token = jwt.encode({
        #         'username': user.username,
        #         'iat': datetime.datetime.utcnow(),
        #         'nbf': datetime.datetime.utcnow() + datetime.timedelta(minutes=-5),
        #         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        # }, 'muhammad')
        # token=jwt.encode(payload,'secret',algorithm='HS256').decode('utf-8')
        # print(token)
        user_data={}
        user_data['success']=True
        # user_data['token']=token
        user_details = SellerSerializer(user).data
        user_details.pop('password', None)
        user_details.pop('devices', None)
        user_details.pop('email', None)
        user_data['user']=user_details
        return Response(user_data, status=status.HTTP_201_CREATED)
    
    except ValidationError as e:
        
        return Response({'success':False,'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error_data = {
            'success': False,
            'error_message':serialize_exception(e),
        }
        return Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['POST'])
def login(request):    
    # request = self.context.get('request')
    # print("Test")
    user_agent_str = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_str)
        
    device_info = {
        'random_access_point': user_agent_str,
        'device_name': user_agent.device.family,
        'action':'login',
        'ip': request.META.get('REMOTE_ADDR', '')
    }
    devices=[device_info]
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.validated_data.get('email') 
        print(request.data['email'])
        password = serializer.validated_data.get('password')

        try:
            
            user =User.objects.get(email=request.data['email'])
            for device_data in [device_info]:
                Device.objects.create(user=user, **device_data)
            
            
            # print(user.email)
            
            if check_password(password, user.password):
                token = jwt.encode({
                        'username': user.username,
                        'iat': datetime.datetime.utcnow(),
                        'nbf': datetime.datetime.utcnow() + datetime.timedelta(minutes=-5),
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
                }, 'muhammad')
                response=Response({'success':True,"message": "Login successful",'email':user.email,'username':user.username,'token':token}, status=status.HTTP_200_OK)
                response.set_cookie(
                    key='token',
                    value=token,
                    httponly=True,  
                    samesite='Lax',
                    secure=True 
                )
                return response
            else:
                error_data = {
                    'success': False,
                    'error_message': {
                        "type": "Invalid credentials",
                        "message": "email and password went wrong"
                    },
                }
                return Response(error_data, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            error_data = {
                    'success': False,
                    'error_message': {
                        "type": "Invalid credentials",
                        "message": "email are not find"
                    },
                }
            return Response(error_data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        error_data = {
            'success': False,
            'error_message': serializer.errors,
        }
        return Response({**error_data}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def logout_view(request):
    response = JsonResponse({'success': True, 'message': 'Logged out successfully.'})
    response.delete_cookie('token') 
    response.delete_cookie('token') 
    return response


@api_view(['GET'])
def categories(request):
    try:
        user_agent_str = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(user_agent_str)
                    
        device_info = {
            'random_access_point': user_agent_str,
            'device_name': user_agent.device.family,
            'action':'categories',
            'ip': request.META.get('REMOTE_ADDR', '')
        }
    
        user=User.objects.get(username=request.decoded_user['username'])
        categories = Category.objects.all()
        category_serializer = CategorySerializer(categories, many=True)
        # print(request.decoded_user)
        Device.objects.create(user=user,**device_info)
        
        
        # logger.info(f"User: {request.user}, Decoded user: {request.decoded_user}")
        
        return Response({'success': True, 'data': category_serializer.data})
    
    except Exception as e:
        return Response({'success': False, 'error': 'Error fetching categories'}, status=500)

@api_view(['POST'])
def create_gig(request):
    print(request.data)
    return Response("Hacker")