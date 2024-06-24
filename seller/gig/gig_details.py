from rest_framework import serializers
from common.models.gig import GigData,Gig_Category,Select_User_Packages
from common.models.category import Category,Subcategory,ServiceType
from common.serializer.category_serialzer import SubCategorySerializer
from .gig_prices import UserPackages 


class Service_TypeCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    class Meta:
        model = ServiceType
        fields = ['id','name']
class SubCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    class Meta:
        model = Subcategory
        fields = ['id','name']
class CategorySerializer(serializers.ModelSerializer):
#     sub_categories=SubCategorySerializer(many=True,required=False)
    name = serializers.CharField(max_length=100)
    class Meta:
        model = Category
        fields = ['id','name',]
class Gig_category_Serializer(serializers.ModelSerializer):
    category_id= serializers.IntegerField()
    sub_category_id= serializers.IntegerField()
    service_type=serializers.BooleanField()
    server_type_id=serializers.IntegerField(required=False)
    
    class Meta:
        model = Gig_Category
        fields = ['category_id', 'sub_category_id', 'service_type', 'server_type_id']

class Get_GigSerializer(serializers.ModelSerializer):
       class Meta:
              model = GigData
              fields = ['title',]
       def to_representation(self, instance):
              representation = super().to_representation(instance)
              category_representation=[]
              category=Gig_Category.objects.filter(gig=instance.id)
              category_data=Gig_category_Serializer(category,many=True).data[0]
              if category_data['category_id']:
                     main_category=Category.objects.get(id=category_data['category_id'])
                     main_category_data=CategorySerializer(main_category,many=False).data
                     category_representation.append(main_category_data['name'])
                     if category_data['sub_category_id']:
                            sub_category=Subcategory.objects.get(id=category_data['sub_category_id'])
                            sub_category_data=SubCategorySerializer(sub_category).data
                            category_representation.append(sub_category_data['name'])
                            if category_data['service_type']:
                                   servicetype=ServiceType.objects.get(id=category_data['server_type_id'])
                                   servicetype_data=Service_TypeCategorySerializer(servicetype).data
                                   category_representation.append(servicetype_data['name'])
              representation['category']=category_representation
              packages=Select_User_Packages.objects.filter(gig=instance)
              packages_data=UserPackages(packages,many=True).data
              representation['packages']=packages_data
              return representation
        