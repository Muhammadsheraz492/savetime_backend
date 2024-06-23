import json
from django.db import IntegrityError
from rest_framework import serializers
from ..models import Category,Subcategory,ServiceType
from ..models.gig import GigData,Gig_Category
from rest_framework.response import Response
from .category_serialzer import CategorySerializer
from rest_framework import status
class Gig_category_Serializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()
    category_name = serializers.CharField(write_only=True)
    sub_category_id = serializers.IntegerField( write_only=True)
    sub_category_name = serializers.CharField( write_only=True)
    nested_sub_category_id = serializers.IntegerField(write_only=True, required=False)
    nested_sub_category_name = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = Category
        fields = ['category_id', 'category_name', 'sub_category_id', 'sub_category_name', 'nested_sub_category_id', 'nested_sub_category_name']
class GigSerializer(serializers.ModelSerializer):
    gig = Gig_category_Serializer()
    def create_gig_cayegory(self,gig_instance,gig):
        try:
            print(gig)
            Category_id = gig.get('category_id',None)
            Category_Name = gig.get('category_name',None)
            Sub_Category_id = gig.get('sub_category_id',None)
            Sub_Category_Name = gig.get('sub_category_name',None)
            service_type_id=gig.get('nested_sub_category_id',None)
            service_type_name=gig.get("nested_sub_category_name",None)
            category_data = Category.objects.get(id=Category_id, name=Category_Name)
            sub_category_data=Subcategory.objects.get(id=Sub_Category_id,name=Sub_Category_Name)
            service_type=False    
             
            if sub_category_data.service_type:  
                if   service_type_id and service_type_name:
                    # print(sub_category_data.service_type)
                    # if service_type_id:
                    service_type_data=ServiceType.objects.get(subcategory=sub_category_data,id=service_type_id,name=service_type_name)
                    service_type=bool(service_type_data)
                    service_type_id=service_type_data.id
                    # print(service_type_data)
                else:
                    raise serializers.ValidationError("Service Type Required")
            Gig_Category.objects.create(gig=gig_instance,**{
                'category_id':category_data.id,
                'sub_category_id':sub_category_data.id,
                'service_type':service_type,
                'server_type_id':service_type_id    
            })
        except (Category.DoesNotExist,Subcategory.DoesNotExist,ServiceType.DoesNotExist) as e:
            raise serializers.ValidationError(e)
            

    class Meta:
        model = GigData
        fields = ['title','gig']
    def create(self, validated_data):
        # print()
        data=validated_data
        gig=validated_data.pop('gig',None)     
        try:    
            instance = GigData.objects.create(**validated_data)
            self.create_gig_cayegory(instance,gig=gig)
            return data
        except IntegrityError as e:
            raise serializers.ValidationError(e)