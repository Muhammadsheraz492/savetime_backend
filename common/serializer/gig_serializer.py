import json
from django.db import IntegrityError
from rest_framework import serializers
from ..models import Category,Subcategory,ServiceType
from ..models.gig import GigData
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
    def validate(self, data):
        # Check if category_id and sub_category_id are provided
        if 'category_id' not in data:
            raise serializers.ValidationError("category_id is required")
        if 'sub_category_id' not in data:
            raise serializers.ValidationError("sub_category_id is required")
        
        # You can add more validations for other fields if needed
        
        return data


class GigSerializer(serializers.ModelSerializer):
    gig = Gig_category_Serializer()
    def create_gig_cayegory(self,gig_instance,gig):
        print("Hello")
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
            
            if not Category_id or not Category_Name or not Sub_Category_id or not Sub_Category_Name:
                raise serializers.ValidationError("Category and Subcategory details are required.")

            if sub_category_data.service_type and service_type_id and service_type_name:
                # print(sub_category_data.service_type)
                # if service_type_id:
                service_type_data=ServiceType.objects.get(id=service_type_id,name=service_type_name)
                print(service_type_data)
            else:
                raise serializers.ValidationError("Service Type Required")
                
                
            
            # # print(gig)
            # print("Category data:", category_data)
            # # print("Sub Category data:", sub_category_data)
            
            
            # return Response({'success': True, 'message': 'Category found.'}, status=status.HTTP_200_OK)
        except (Category.DoesNotExist,Subcategory.DoesNotExist) as e:
            raise serializers.ValidationError(e)
            

    class Meta:
        model = GigData
        fields = ['title','gig']
    def create(self, validated_data):
        data=validated_data
        gig=validated_data.pop('gig',None)
        # print(validated_data)
        
        
        try:    # print(validated_data)
            # instance=GigData.objects.create(**validated_data)
            instance = GigData.objects.create(**validated_data)
            self.create_gig_cayegory(instance,gig=gig)
            # print(instance)
            return data
        except IntegrityError as e:
            raise serializers.ValidationError(e)