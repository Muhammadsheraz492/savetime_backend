from django.db import IntegrityError
from rest_framework import serializers
from admin.models.admin_user_model import Admin_User, Admin_Device
from django.contrib.auth.hashers import make_password

class AdminDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin_Device
        fields = ['id', 'device_name', 'random_access_point', 'ip', 'action', 'created_at']

class AdminUserSerializer(serializers.ModelSerializer):
    devices = AdminDeviceSerializer(many=True)
    class Meta:
        model = Admin_User
        fields = ('id', 'username', 'email', 'password', 'devices', 'created_at', 'status')
        extra_kwargs = {'password': {'write_only': True}}  # Ensure password is write-only
    def _create_devices(self, user_instance, devices_data):
        for device_data in devices_data:
            try:
                Admin_Device.objects.create(user=user_instance, **device_data)
            except IntegrityError as e:
                # print(e)
                    raise serializers.ValidationError(e)


    def create(self, validated_data):
        # Override create method to hash the password before saving
        validated_data['password'] = make_password(validated_data.get('password'))
        devices_data = validated_data.pop('devices', [])
        try:
            instance= super().create(validated_data)
            self._create_devices(instance, devices_data)
            
            return instance
        except IntegrityError as e:
            raise serializers.ValidationError(e)
    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation.pop('devices')
        user_devices = Admin_Device.objects.filter(user_id=instance.id)
        devices_representation = AdminDeviceSerializer(user_devices, many=True).data
        representation['devices'] = devices_representation
        
        return representation