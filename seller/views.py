from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user_agents import parse
from common.middleware.exception_handler import custom_exception_handler
from common.serializer.gig_serializer import GigSerializer
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
from common.models.category import Category,Subcategory,Packages,ServiceType
from common.models.gig import GigData
from common.serializer.category_serialzer import CategorySerializer,SubCategorySerializer,Packages_serializer,ServiceTypeSerializer
from .gig.gig_details import Get_GigSerializer
from .gig.gig_prices import Price_serializer
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
@api_view(['GET'])
def packages(request):
    try:
        sub_cat_id=request.GET.get("sub_cat_id")
        service_id=request.GET.get('service_id')
        if sub_cat_id is None:
            return Response({'success':False,'message':'SubCategory is Required'})
        subcategory = Subcategory.objects.filter(id=sub_cat_id)
        subcategory_representation=SubCategorySerializer(subcategory,many=True).data[0]  
        if subcategory_representation['is_price']:
            packages_=Packages.objects.filter(subcategory=subcategory_representation['id'])
            packages_data=Packages_serializer(packages_,many=True).data
            subcategory_representation['packages']=packages_data
        else:
            subcategory_representation.pop('service_type_data')
            if service_id is None:
                return Response({'success':False,'message':'Service Type id is Required'})
            servertype=ServiceType.objects.filter(subcategory=sub_cat_id,id=service_id)
            if not servertype.exists():
                return Response({'success':False,'message':'Servce Type Not Found'})
            servertype_data=ServiceTypeSerializer(servertype,many=True).data[0]
            if servertype_data['has_gig_price']:
                packages_=Packages.objects.filter(subcategory=subcategory_representation['id'],servicetype=servertype_data['id'])
                packages_data=Packages_serializer(packages_,many=True).data
                servertype_data['packages']=packages_data
            subcategory_representation['servertype_data']=servertype_data
        return Response({'success':True,'message':"All Packages Arive",'data':subcategory_representation})       
    except (Subcategory.DoesNotExist,ServiceType.DoesNotExist) as e:
      print(e)
      raise e
        


@api_view(['POST'])
def create_gig(request):
    try:
        serializer = GigSerializer(data=request.data)  # Extract 'gig' from request data
        if serializer.is_valid():
            data=serializer.save()
            # Perform any additional actions like saving to the database
            # For now, let's just return the serialized data as a response
            return Response({'success':True,"message":"Working Good",'data':data})
        
        raise serializers.ValidationError(serializer.errors)
    except serializers.ValidationError as e:
        errors = e.detail
        
        if 'gig' in errors:
            error_message = " ".join([f"{key}: {value[0]}" for key, value in errors['gig'].items()])
            print(error_message)
            raise serializers.ValidationError(error_message)

        # Handle other validation errors if needed
        raise e  
        # else:
        #     # If serializer validation fails, return the errors
        #     print(serializer.errors)
        #     raise custom_exception_handler( serializer.errors)
        #     # error_message = " ".join([f"{key}: {value[0]}" for key, value in errors.items()])
        #     # return Response({'success': False, 'message': error_message}, status=status.HTTP_400_BAD_REQUEST) 
            
           
    except Exception as e:
      print(e)
      raise e
        
        

@api_view(['GET'])
def gig_details(request,id):
    try:
        gig=GigData.objects.filter(id=id)
        gig_data=Get_GigSerializer(gig,many=True).data
        return Response({'success':True,'data':gig_data})
    except (GigData.DoesNotExist) as e:
      print(e)
      raise e
@api_view(['POST'])
def create_prices(request,id):
    try:
        # print(request.data['packages'])
        # data=
        price_serializer = Price_serializer(data={'category_id':id,**request.data})
        
        # Validate the serializer data
        if price_serializer.is_valid():
            price_serializer.save()
            return Response({'success':True,'message':"working on creating prices"})
        else:
            print(price_serializer.error_messages)
            raise price_serializer.error_messages
            
        
    except (GigData.DoesNotExist) as e:
      print(e)
      raise e
    