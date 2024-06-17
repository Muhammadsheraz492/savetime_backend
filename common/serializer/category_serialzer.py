from django.db import IntegrityError

from rest_framework import serializers
from common.models.category import *
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name']
class CategorySerializer(serializers.ModelSerializer):
    sub_categories=SubCategorySerializer(many=True)
    class Meta:
        model = Category
        fields = ['id','name','email','sub_categories']
    def _create_subcategories(self, user_instance, subcategorys):
        for subcategory in subcategorys:
            try:
                Subcategory.objects.create(category=user_instance,**subcategory)                
            except IntegrityError as e:
                raise serializers.ValidationError(e)
    def create(self, validated_data):
        # try:
        #     subcategorys=validated_data.pop('sub_categories',[])
        #     instance= super().create(validated_data)
        #     self._create_devices(instance,subcategorys)
        #     return instance
        # except IntegrityError as e:
        #     raise serializers.ValidationError(e)
         
        subcategories_data = validated_data.pop('sub_categories', [])
        try:
            # Check if category with the same name already exists
            instance = Category.objects.get(name=validated_data['name'])
            # raise serializers.ValidationError('success':False,'message':"Category with this name already exists.")
            raise serializers.ValidationError({'success': False, 'message': 'Category with this name already exists.'})
        except Category.DoesNotExist:
            instance = Category.objects.create(**validated_data)
            self._create_subcategories(instance, subcategories_data)
            return instance
        except IntegrityError as e:
            raise serializers.ValidationError(str(e))
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # # representation.pop('devices')
        # user_devices = Admin_Device.objects.filter(user_id=instance.id)
        # devices_representation = AdminDeviceSerializer(user_devices, many=True).data
        # representation['devices'] = devices_representation
        subcategory=Subcategory.objects.filter(category_id=instance.id)
        subcategory_representation=SubCategorySerializer(subcategory,many=True).data
        representation['sub_categories']=subcategory_representation
        
        
        return representation
    