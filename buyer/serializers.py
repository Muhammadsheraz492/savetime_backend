from rest_framework import serializers
from .models import Buyer_User
from django.contrib.auth.hashers import make_password

class BuyerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer_User
        fields = ['id', 'firstname', 'lastname', 'username', 'profile_image', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    def validate(self, data):
        """
        Check if username or email already exists.
        """
        username = data.get('username')
        email = data.get('email')

        if Buyer_User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'success':False,"username": ["Buyer user with this username already exists."]})
        
        if Buyer_User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'success':False,"email": ["Buyer user with this email already exists."]})
        
        return data
    def create(self, validated_data):
        # self.validate(validated_data)
        validated_data['password'] = make_password(validated_data['password'])
        user = Buyer_User.objects.create(**validated_data)
        return user
