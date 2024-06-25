from rest_framework import serializers
from .models import Device, User
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
import boto3
from django.conf import settings
from datetime import datetime
from botocore.exceptions import ClientError
from user_agents import parse
from rest_framework.exceptions import ValidationError
from .custom_exceptions import CustomValidationError  # Import the custom exception

# def upload_to(instance, filename):
    # print('images/{filename}'.format(filename=filename))
    # return 'images/{filename}'.format(filename=filename)
class DeviceSerializer(serializers.ModelSerializer):
    random_access_point=serializers.CharField(required=True)
    device_name=serializers.CharField(required=True)
    ip=serializers.CharField(required=True)
    class Meta:
        model = Device
        fields = ['random_access_point', 'device_name', 'ip']

class SellerSerializer(serializers.ModelSerializer):
    devices=[]
    email=serializers.EmailField(required=True)
    username=serializers.CharField(required=True)
    firstname=serializers.CharField(required=True)
    lastname=serializers.CharField(required=True)
     
    # devices = DeviceSerializer(many=True, read_only=True)  # Assuming you want to display related devices

    
    profile_image = serializers.ImageField(max_length=None, required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'username', 'email', 'password', 'profile_image']
    
    def create(self, validated_data):
        # devices_data = validated_data.pop('devices', [])
        password = validated_data.pop('password')
        validated_data['password']=make_password(password=password)
        profile_image = validated_data.get('profile_image')
        if profile_image:
            
            profile_image = validated_data.pop('profile_image')
            try:
                print(settings.AWS_STORAGE_BUCKET_NAME)
                s3 = boto3.client(
                    's3',
                    aws_access_key_id='AKIA2UC27FQCXBZKOAUO',
                    aws_secret_access_key='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',
                    region_name='eu-north-1'
                )
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                image_key = f"profile_images/{timestamp}_{profile_image.name}".replace(" ","")
                s3.upload_fileobj(profile_image, 'wishtun', image_key)
                s3_url = f"https://wishtun.s3.amazonaws.com/{image_key}"
                validated_data['profile_image'] = s3_url

            except ClientError as e:
                print(f"Error uploading profile image to S3: {e}")
                raise serializers.ValidationError("Failed to upload profile image")
        try:
            with transaction.atomic():  # Ensure atomicity
                user = User.objects.create(**validated_data)
                for device_data in self.devices:
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
    def validate(self, attrs):
        request = self.context.get('request')
        user_agent_str = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(user_agent_str)
        
        device_info = {
            'random_access_point': user_agent_str,
            'device_name': user_agent.device.family,
            'action':'register',
            'ip': request.META.get('REMOTE_ADDR', '')
        }
        self.devices.append(device_info)
        
        return super().validate(attrs)
    def to_representation(self, instance):
        data=super().to_representation(instance=instance)
        if instance.profile_image:
            data['profile_image']=instance.profile_image
        return data
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User  # Specify your custom user model here
        fields = ["email", "password"]

    def validate_email(self, value):
        print("This is mine")
        if not value:
            error_data = {
                'success': False,
                'error_message': {
                    "type": "ValidationError",
                    "message": "Email field cannot be blank."
                },
            }
            raise CustomValidationError(detail=error_data)
        try:
            user = User.objects.get(email=value)
            return user
        except User.DoesNotExist:
            error_data = {
                'success': False,
                'error_message': {
                      "type": "ValidationError",
                      "message":"This email does not exist."
                
                },
            }
            raise CustomValidationError(detail=error_data)
    def run_validation(self, data):
        if 'email' in data and not data['email'].strip():
            error_data = {
                'success': False,
                'error_message': {
                    "type": "ValidationError",
                    "message": "Email field cannot be blank."
                },
            }
            raise CustomValidationError(detail=error_data)
        if 'password' in data and not data['password'].strip():
            error_data = {
                'success': False,
                'error_message': {
                    "type": "ValidationError",
                    "message": "Password field cannot be blank."
                },
            }
            raise CustomValidationError(detail=error_data)
        return super().run_validation(data)
    # def validate(self, attrs):
    #     email = attrs.get('email')
    #     try:
    #         user = User.objects.get(email=email)
    #         return user
    #     except User.DoesNotExist:
    #         error_data = {
    #             'success': False,
    #             'error_message': {
    #                   "type": "ValidationError",
    #                   "message":"This email does not exist."
                
    #             },
    #         }
    #         print(error_data)
    #         raise CustomValidationError(detail=error_data)
    #     return attrs
    