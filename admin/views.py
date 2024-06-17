from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers.user_serializer import *
from common.serializer.category_serialzer import *
from user_agents import parse
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password
import jwt,datetime
from django.conf import settings
from django.utils.decorators import decorator_from_middleware
from admin.controller.devices import *
@api_view(['POST'])
def post_login(request):
    try:
        email=request.data['email']
        password=request.data['password']
        user=Admin_User.objects.get(email=email)
        if check_password(password,user.password):
            token = jwt.encode({
                        'email': user.email,
                        'iat': datetime.datetime.utcnow(),
                        'nbf': datetime.datetime.utcnow() + datetime.timedelta(minutes=-5),
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
            }, settings.ADMIN_PANNEL_ACCESS)
            user_agent_str = request.META.get('HTTP_USER_AGENT', '')
            user_agent = parse(user_agent_str)
                
            device_info = {
                'random_access_point': user_agent_str,
                'device_name': user_agent.device.family,
                'action':'admin_login',
                'ip': request.META.get('REMOTE_ADDR', '')
            }
            Admin_Device.objects.create(user=user, **device_info)
            
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
            
            return Response({'success': False, 'message':"Wrong Cradentials"}, status=status.HTTP_400_BAD_REQUEST)
    except Admin_User.DoesNotExist:
        return Response({'success':False,"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
    
class AdminUserAPIView(APIView):
    
    def post(self, request):
        data=request.data.copy()
        user_agent_str = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(user_agent_str)
            
        device_info = {
            'random_access_point': user_agent_str,
            'device_name': user_agent.device.family,
            'action':'admin_register',
            'ip': request.META.get('REMOTE_ADDR', '')
        }
        data['devices'] = [device_info]
        serializer = AdminUserSerializer(data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True, **serializer.data}, status=status.HTTP_201_CREATED)
            else:
                errors = serializer.errors
                print("Hello")
                error_message = " ".join([f"{key}: {value[0]}" for key, value in errors.items()])
                return Response({'success': False, 'message': error_message}, status=status.HTTP_400_BAD_REQUEST) 
        except serializers.ValidationError as e:
            error_message = ""
            for error_detail in e.detail:
                error_message += str(error_detail) + " "
            error_message=error_message.replace("admin_admin_user","")
            return Response({'success': False, 'message': str("IntegrityError occurred while creating user "+error_message)}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        try:
            users = Admin_User.objects.all()
            serializer = AdminUserSerializer(users,many=True)
            return Response({'success':True,'data':serializer.data})
        except Exception as e:
            error_message = str(e)
            return Response({'success': False, 'message': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['post','get'])
def post_category(request):
    if request.method == 'POST':
        try:
            print()
            
                
            user=Admin_User.objects.get(email=request.decoded_user['email'])
            get_device_info(request=request,user=user,name='post category')
            print(request.data['name'])
            # category_eixt=Category.objects.get(name=request.data['name'])
            # print(user)
            # print(request.data)
            # print(category_eixt)
            
            request.data['email']=user.email
            if 'name' not in request.data:
                return Response({'success': False, 'message': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            category_serializer=CategorySerializer(data=request.data)
            if category_serializer.is_valid():
                category_serializer.save()
                return Response({'status':True,'message':"Category created successfully",**category_serializer.data}, status=status.HTTP_201_CREATED)
            else:
                errors = category_serializer.errors
                error_message = " ".join([f"{key}: {value[0]}" for key, value in errors.items()])
                return Response({'success': False, 'message': error_message}, status=status.HTTP_400_BAD_REQUEST) 
            
        except Admin_User.DoesNotExist:
            return Response({'success':False,"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        # query=Category.objects.all()
        # serializer=CategorySerializer(query,many=True)
        # return Response({'success':True,"message": "All Category Data",'data':serializer.data}, status=status.HTTP_200_OK)
        try:
            user=Admin_User.objects.get(email=request.decoded_user['email'])
            get_device_info(request=request,user=user,name='get category')
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response({
                'success': True,
                'message': 'All Category Data',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to retrieve categories',
                'error': str(e)  # Convert exception to string for response
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
   
