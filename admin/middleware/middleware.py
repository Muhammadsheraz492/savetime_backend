# admin/middleware/middleware.py
from django.http import JsonResponse

class BearerTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        bearer_token = request.headers.get('Authorization')
        excluded_urls = ['/v1/api/admin/login/',]
        print(request.path)
        if request.path in excluded_urls:
            response = self.get_response(request)
            return response

        if not self._validate_token(bearer_token):
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        response = self.get_response(request)
        return response

    def _validate_token(self, bearer_token):
        pass  # Replace this with your actual token validation logic
