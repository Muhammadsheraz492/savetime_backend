from user_agents import parse
def get_device_info(request):
    user_agent_str = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_str)
                
    device_info = {
        'random_access_point': user_agent_str,
        'device_name': user_agent.device.family,
        'action':'admin_login',
        'ip': request.META.get('REMOTE_ADDR', '')
    }
    return device_info