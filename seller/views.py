from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user_agents import parse
from .serializers import SellerSerializer
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from rest_framework.authtoken.models import Token
import traceback
from rest_framework.authentication import TokenAuthentication
import jwt,datetime
from .models import *

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
        serializer = SellerSerializer(data=data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = jwt.encode({
                'username': user.username,
                'iat': datetime.datetime.utcnow(),
                'nbf': datetime.datetime.utcnow() + datetime.timedelta(minutes=-5),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, 'muhammad')
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