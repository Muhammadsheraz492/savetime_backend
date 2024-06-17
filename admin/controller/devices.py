from django.db import IntegrityError
from user_agents import parse
from rest_framework.response import Response
from rest_framework import status
from admin.models.admin_user_model import Admin_Device
def get_device_info(request,user,name):
    user_agent_str = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_str)
                
    device_info = {
        'random_access_point': user_agent_str,
        'device_name': user_agent.device.family,
        'action':name,
        'ip': request.META.get('REMOTE_ADDR', '')
    }
    try:
            Admin_Device.objects.create(user=user, **device_info)
    except IntegrityError as e:
                # print(e)
            return Response({'success':False,'message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)