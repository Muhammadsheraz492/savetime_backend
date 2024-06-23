# custom_exceptions.py
from rest_framework.exceptions import APIException

class CustomValidationError(APIException):
    status_code = 400
    default_detail = 'Invalid input.'
    default_code = 'invalid'

    def __init__(self, detail, code=None):
        self.detail = detail
        self.code = code if code is not None else self.default_code
