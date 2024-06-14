from django.db import IntegrityError

from rest_framework import serializers
from admin.models.category import Category,Subcategory
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'name']
class CategorySerializer(serializers.ModelSerializer):
    sub_categories=SubCategorySerializer(many=True)
    class Meta:
        model = Category
        fields = ['id','name','email','sub_categories']
    def _create_devices(self, user_instance, subcategorys):
        for subcategory in subcategorys:
            try:
                Subcategory.objects.create(category=user_instance,**subcategory)                
            except IntegrityError as e:
                raise serializers.ValidationError(e)
    def create(self, validated_data):
        try:
            subcategorys=validated_data.pop('sub_categories',[])
            instance= super().create(validated_data)
            self._create_devices(instance,subcategorys)
            return instance
        except IntegrityError as e:
            raise serializers.ValidationError(e)
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
    