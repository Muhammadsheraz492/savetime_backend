from django.http import JsonResponse
import jwt
from django.conf import settings

class BearerTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def _validate_token(self, bearer_token,secrete):
                try:
                    
                    decoded_token = jwt.decode(bearer_token,secrete, algorithms=["HS256"])
                    return decoded_token
                except jwt.ExpiredSignatureError:
                    return None
                except jwt.InvalidTokenError:
                    return None

    def __call__(self, request):
        bearer_token = request.headers.get('Authorization')
        cookies_token = request.headers.get('Cookie')
        if '/seller/' in request.path:
            excluded_urls = ['/seller/register/','/seller/login/','/seller/varify_user/']
            if request.path in excluded_urls:
                return self.get_response(request)
            try:
                if bearer_token and cookies_token and bearer_token.replace("Bearer ", "") == cookies_token.replace("token=", ""):
                    decoded_user = self._validate_token(bearer_token.replace("Bearer ", ""),'muhammad')
                    
                    if decoded_user:
                        request.decoded_user = decoded_user
                        return self.get_response(request)
                    else:
                        return JsonResponse({'status': False, 'message': 'Unauthorized. Invalid token.'}, status=403)
                else:
                    return JsonResponse({'status': False, 'message': 'Unauthorized'}, status=403)
            except jwt.ExpiredSignatureError:
                return JsonResponse({'status': False, 'message': 'Unauthorized. Token has expired.'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'status': False, 'message': 'Unauthorized. Invalid token.'}, status=401)
            except Exception as e:
                return JsonResponse({'status': False, 'message': 'Unauthorized '}, status=500)
        elif '/buyer/' in request.path:
            excluded_urls = ['/buyer/register/','/buyer/login/']
            if request.path in excluded_urls:
                return self.get_response(request)
            try:
                if bearer_token and cookies_token and bearer_token.replace("Bearer ", "") == cookies_token.replace("token=", ""):
                    decoded_user = self._validate_token(bearer_token.replace("Bearer ", ""),'muhammad')
                    
                    if decoded_user:
                        request.decoded_user = decoded_user
                        return self.get_response(request)
                    else:
                        return JsonResponse({'status': False, 'message': 'Unauthorized. Invalid token.'}, status=403)
                else:
                    return JsonResponse({'status': False, 'message': 'Unauthorized'}, status=403)
            except jwt.ExpiredSignatureError:
                return JsonResponse({'status': False, 'message': 'Unauthorized. Token has expired.'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'status': False, 'message': 'Unauthorized. Invalid token.'}, status=401)
            except Exception as e:
                return JsonResponse({'status': False, 'message': 'Unauthorized '}, status=500)
        
        
        else:
        
            excluded_urls = ['/v1/api/admin/login/','/v1/api/admin/user','/v1/api/admin/user/','/seller/register/','/seller/login/']
            print(request.path)
            if request.path in excluded_urls:
                return self.get_response(request)

            try:
                if bearer_token and cookies_token and bearer_token.replace("Bearer ", "") == cookies_token.replace("token=", ""):
                    decoded_user = self._validate_token(bearer_token.replace("Bearer ", ""),settings.ADMIN_PANNEL_ACCESS)
                    
                    if decoded_user:
                        request.decoded_user = decoded_user
                        return self.get_response(request)
                    else:
                        return JsonResponse({'status': False, 'message': 'Unauthorized. Invalid token.'}, status=403)
                else:
                    return JsonResponse({'status': False, 'message': 'Unauthorized'}, status=403)
            except jwt.ExpiredSignatureError:
                return JsonResponse({'status': False, 'message': 'Unauthorized. Token has expired.'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'status': False, 'message': 'Unauthorized. Invalid token.'}, status=401)
            except Exception as e:
                return JsonResponse({'status': False, 'message': 'Unauthorized '}, status=500)

            

