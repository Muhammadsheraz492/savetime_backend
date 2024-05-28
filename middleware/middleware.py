# myapp/middleware.py

import jwt
from django.http import JsonResponse

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('token')

        if not token:
            return JsonResponse({'success': False, 'message': 'Authentication credentials were not provided.'}, status=401)

        try:
            decoded_token = jwt.decode(token, 'muhammad', algorithms=["HS256"])
            request.user = decoded_token['username']
        except jwt.ExpiredSignatureError:
            return JsonResponse({'success': False, 'message': 'Token has expired.'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'success': False, 'message': 'Invalid token.'}, status=401)

        response = self.get_response(request)
        return response
