from rest_framework import serializers
from .models import Device, User
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['random_access_point', 'device_name', 'ip']

class SellerSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(required=True)
    username=serializers.CharField(required=True)
    firstname=serializers.CharField(required=True)
    lastname=serializers.CharField(required=True)
    devices = DeviceSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'username', 'email', 'password', 'devices']
    
    def create(self, validated_data):
        devices_data = validated_data.pop('devices', [])
        password = validated_data.pop('password')
        validated_data['password']=make_password(password=password)
        # user = User(**validated_data)
        try:
            with transaction.atomic():  # Ensure atomicity
                user = User.objects.create(**validated_data)
                for device_data in devices_data:
                    Device.objects.create(user=user, **device_data)
                return user
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e):
                raise serializers.ValidationError("Email address already exists.")
            else:
                raise serializers.ValidationError("An unexpected error occurred.")
    def validate_email(self, value):
        if User.objects.filter(email=value):
            raise serializers.ValidationError("Email already exists")
        return value
    def validate_username(self, value):
        if User.objects.filter(username=value):
            raise serializers.ValidationError("Username already exists")
        return value
    def validate_firstname(self,value):
        if value is None:
            raise serializers.ValidationError("fistname are required")
        return value
    def validate_lastname(self,value):
        if value is None:
            raise serializers.ValidationError("lastname are required")
        return value
        