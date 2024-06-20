# from rest_framework import status
# from rest_framework.response import Response
# from django.core.exceptions import ObjectDoesNotExist
# from rest_framework.views import exception_handler

# def custom_exception_handler(exc, context):
#     success = False  # Set success to False by default

#     # Check if the exception is an ObjectDoesNotExist exception
#     if isinstance(exc, ObjectDoesNotExist):
#         detail = {'error': 'Not found.', 'detail': str(exc)}
#         return Response(detail, status=status.HTTP_404_NOT_FOUND)

#     # Call REST framework's default exception handler first,
#     # to get the standard error response.
#     response = exception_handler(exc, context)

#     # Now add the HTTP status code to the response.
#     if response is not None:
#         if isinstance(response.data, list):
#             # If response.data is a list, wrap it in a dictionary
#             response.data = {'error': response.data[0]}
#         # response.data['status_code'] = response.status_code

#     # Add 'success' key to the response data
#     response.data['success'] = success
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    success = False  # Set success to False by default

    try:
        # Check if the exception is an ObjectDoesNotExist exception
        if isinstance(exc, ObjectDoesNotExist):
            detail = {'error': 'Not found.', 'detail': str(exc)}
            return Response(detail, status=status.HTTP_404_NOT_FOUND)

        # Call REST framework's default exception handler first,
        # to get the standard error response.
        response = exception_handler(exc, context)

        # Now add the HTTP status code to the response.
        if response is not None:
            if isinstance(response.data, list):
                # If response.data is a list, wrap it in a dictionary
                response.data = {'message': response.data[0]}
            response.data['status_code'] = response.status_code

    except Exception as e:
        # Handle any unexpected exceptions gracefully
        detail = {'error': 'Internal Server Error.', 'detail': str(e)}
        return Response(detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # If response is None (no exception handled by DRF), create a default error response
    if response is None:
        detail = {'message': 'Unexpected error occurred.', 'detail': str(exc)}
        response = Response(detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Add 'success' key to the response data
    response.data['success'] = success

    return response
