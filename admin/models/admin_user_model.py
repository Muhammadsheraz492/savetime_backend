import logging
from django.db import models
from djongo import models as djongo_models
from bson import ObjectId
from django.utils import timezone

class Admin_Device(models.Model):
    user = models.ForeignKey('Admin_User', on_delete=models.CASCADE, null=True, related_name='user_devices')
    device_name = models.CharField('device_name',max_length=100)
    random_access_point = models.CharField(max_length=100)
    ip = models.CharField(max_length=200)
    action=models.CharField(max_length=200)
    created_at = models.DateTimeField('created_At', auto_now_add=True, null=True)
    def __str__(self) -> str:
        return self.ip
class Admin_User(models.Model):
    username = models.CharField(max_length=200, default='',)
    email = models.EmailField(unique=True, default='')
    password = models.CharField(max_length=200, default='')
    devices = models.ManyToManyField(Admin_Device)
    created_at = models.DateTimeField('created_At', auto_now_add=True, null=True)
    status=models.BooleanField('status',default=True)
    def __str__(self) -> str:
        return self.email
   
