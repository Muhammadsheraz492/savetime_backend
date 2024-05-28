from rest_framework import serializers
from .models import Device, User
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
import boto3
from django.conf import settings
from datetime import datetime
from botocore.exceptions import ClientError

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
    def create(self, validated_data):
        print(validated_data)
        pass

class SellerSerializer(serializers.ModelSerializer):
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
        print(validated_data)
        # devices_data = validated_data.pop('devices', [])
        password = validated_data.pop('password')
        validated_data['password']=make_password(password=password)
        profile_image = validated_data.get('profile_image')
        if profile_image:
            print(f"Profile Image Filename: {profile_image.name}")
            
            profile_image = validated_data.pop('profile_image')
            try:
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                image_key = f"profile_images/{timestamp}_{profile_image.name}".replace(" ","")
                s3.upload_fileobj(profile_image, settings.AWS_STORAGE_BUCKET_NAME, image_key)
                s3_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{image_key}"
                validated_data['profile_image'] = s3_url

            except ClientError as e:
                print(f"Error uploading profile image to S3: {e}")
                raise serializers.ValidationError("Failed to upload profile image")
        try:
            with transaction.atomic():  # Ensure atomicity
                user = User.objects.create(**validated_data)
                
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
    def to_representation(self, instance):
        data=super().to_representation(instance=instance)
        if instance.profile_image:
            data['profile_image']=instance.profile_image
        return data
        