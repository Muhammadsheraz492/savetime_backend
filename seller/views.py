from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user_agents import parse
from .serializers import SellerSerializer
from django.core.exceptions import ValidationError
from django.db import DatabaseError
import traceback
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
        user_agent_str = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(user_agent_str)
        
        device_info = {
            'random_access_point': user_agent_str,
            'device_name': user_agent.device.family,
            'ip': request.META.get('REMOTE_ADDR', '')
        }
        
        data = request.data.copy()
        data['devices'] = [device_info]
        
        serializer = SellerSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        user_data = SellerSerializer(user).data
        user_data.pop('password', None)
        user_data.pop('devices', None)
        
        return Response(user_data, status=status.HTTP_201_CREATED)
    
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error_data = {
            'success': False,
            'error_message':serialize_exception(e),
        }
        return Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)