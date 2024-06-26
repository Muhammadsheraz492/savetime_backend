import logging
from django.db import models
from djongo import models as djongo_models
from bson import ObjectId
from django.utils import timezone
class Otp(models.Model):
    # _id = djongo_models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='otp')
    otp = models.IntegerField()
  

class Device(models.Model):
    # _id = djongo_models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='user_devices')
    device_name = models.CharField(max_length=100)
    random_access_point = models.CharField(max_length=100)
    ip = models.CharField(max_length=200)
    action=models.CharField(max_length=200)
    created_at = models.DateTimeField('created_At', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(models.Model):
    # _id = djongo_models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    firstname = models.CharField(max_length=100, default='')
    lastname = models.CharField(max_length=100, default='')
    username = models.CharField(max_length=200, unique=True,)
    profile_image=models.CharField(max_length=225,null=True,blank=True)
    email = models.EmailField(unique=True, default='')
    password = models.CharField(max_length=200, default='')
    devices = models.ManyToManyField(Device, related_name='user_devices')
    total_earning = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_order = models.PositiveIntegerField(default=0)
    completed_order = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0.0)
    gig_limit = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)  
    created_at = models.DateTimeField('created_At', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    phoneNumber = models.CharField(max_length=15, null=True, blank=True)  # New field for phone number
    is_number_verified = models.BooleanField(default=False)
   
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.username
    
# class Gigs(models.Model):
    