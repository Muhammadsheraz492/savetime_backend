from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers.user_serializer import *
from user_agents import parse
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password
import jwt,datetime
@api_view(['POST'])
def post_login(request):
    try:
        email=request.data['email']
        password=request.data['password']
        user=Admin_User.objects.get(email=email)
        if check_password(password,user.password):
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

   

    # def delete(self, request, pk):
    #     try:
    #         user = Admin_User.objects.get(pk=pk)
    #     except Admin_User.DoesNotExist:
    #         return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
    #     user.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

