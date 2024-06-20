from rest_framework import status
from rest_framework.response import Response

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    success = False

    try:
        if isinstance(exc, ObjectDoesNotExist):
            detail = {'success': False, 'message': 'Not found.', 'detail': str(exc)}
            return Response(detail, status=status.HTTP_404_NOT_FOUND)

        if isinstance(exc, dict) and 'gig' in exc:
            print(exc)
            detail = {'success': False, 'messages': exc, 'status_code': 400}
            return Response(detail, status=status.HTTP_400_BAD_REQUEST)

        response = exception_handler(exc, context)

        if response is not None:
            if isinstance(response.data, list):
                response.data = {'message': response.data[0]}
            response.data['status_code'] = response.status_code

    except Exception as e:
        detail = {'message': 'Internal Server message.', 'detail': str(e)}
        return Response(detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if response is None:
        detail = {'message': 'Unexpected message occurred.', 'detail': str(exc)}
        response = Response(detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response.data['success'] = success

    return response
