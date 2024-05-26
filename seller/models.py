import logging
from django.db import models
from djongo import models as djongo_models
from bson import ObjectId
from django.utils import timezone

class Device(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='user_devices')
    device_name = models.CharField(max_length=100)
    random_access_point = models.CharField(max_length=100)
    ip = models.CharField(max_length=200)
    created_at = models.DateTimeField('created_At', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    firstname = models.CharField(max_length=100, default='')
    lastname = models.CharField(max_length=100, default='')
    username = models.CharField(max_length=200, unique=True,)
    email = models.EmailField(unique=True, default='')
    password = models.CharField(max_length=200, default='')
    devices = models.ManyToManyField(Device, related_name='user_devices')
    total_earning = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_order = models.PositiveIntegerField(default=0)
    completed_order = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0.0)
    gig_limit = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField('created_At', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        # logging.debug("Password hashed: %s", self.password)
        
        # if not self.pk:
        #     self.password = make_password(self.password)
        #     logging.debug("Password hashed: %s", self.password)
        #     print(self)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.username
    