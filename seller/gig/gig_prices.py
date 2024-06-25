from datetime import datetime
from django.db import IntegrityError
from rest_framework import serializers
from common.models.gig import Select_User_Packages,GigData,Select_content_Package
from common.models.category import Subcategory,Content
from django.core.exceptions import ObjectDoesNotExist
from common.models.category import DataOptions
from common.models.gig import Gig_Images
from seller.models import User
from botocore.exceptions import ClientError

import logging
import boto3
from django.conf import settings
logger = logging.getLogger(__name__)  # Replace with your module name if different

from rest_framework.exceptions import ValidationError
# class DataoptionsSerializer(serializers.ModelSerializer):
#     included_modifications=serializers.CharField(required=False)
#     class Meta:
#         model = DataOptions
#         fields='__all__'
class ContentSerializer(serializers.ModelSerializer):
    # included_modifications=serializers.CharField()
    class Meta:
        model = Content
        fields='__all__'
        

class UserPackages_content(serializers.ModelSerializer):

    # name = serializers.CharField(max_length=100
    # active=serializers.BooleanField()
    active = serializers.BooleanField(required=False, default=False)
    included_modifications = serializers.CharField(required=False, allow_null=True)
    content_id=serializers.IntegerField(required=False,allow_null=True)
    

    class Meta:
        model = Select_content_Package
        fields=['id','content_id','title','translated_label','edit_type','included_modifications','active']

class UserPackages(serializers.ModelSerializer):

    # name = serializers.CharField(max_length=100
    content=UserPackages_content(many=True)
    # package_id=serializers.IntegerField()
    class Meta:
        model = Select_User_Packages
        fields = ['id','duration_unit','title','description','duration','price','content']

class Price_serializer(serializers.ModelSerializer):
    packages=UserPackages(many=True)
    category_id=serializers.IntegerField()
    class Meta:
        model=GigData
        fields=['id','category_id','packages']

    def create(self, validated_data):

        try:
            category_id=validated_data.pop('category_id',None)
            packages=validated_data.pop('packages',[])
            if category_id is None:
                return serializers.ValidationError("Gig are not Found")
            gig=GigData.objects.get(id=category_id)
            user_instance=Select_User_Packages.objects.filter(gig=gig)
            user_instance.delete()
            for item in packages:
                contents=item.pop('content',[])
                try:
                  is_duration_limit=False
                  is_content=False
                  if item.get('duration_limit') is not None:
                    is_duration_limit = True
                  if item.get('content') is not None:
                    is_content = True
                  item['is_duration_limit']=is_duration_limit
                  item['is_content']=is_content
                  instance=Select_User_Packages.objects.create(gig=gig,**item)
                  for content_itm in contents:
                    try:
                        stored_content=Content.objects.get(id=content_itm['content_id'],title=content_itm['title'],translated_label=content_itm['translated_label'],edit_type=content_itm['edit_type'])
                        if stored_content.edit_type=='dropdown':
                            if stored_content.data_options:
                                    included_modifications = content_itm.get('included_modifications', None)
                                    if included_modifications is None:
                                        raise ValueError("included_modifications data is missing or invalid")
                                    print(content_itm['included_modifications'])
                                    try:
                                        validate_data_options=DataOptions.objects.get(content=stored_content,text=included_modifications)
                                        print(validate_data_options)
                                    except DataOptions.DoesNotExist:
                                        raise ValueError("included_modifications data is missing or invalid")
                                    except Exception as e:
                                        raise ValueError("included_modifications data is missing or invalid")
     
                    except (Content.DoesNotExist,DataOptions.DoesNotExist) as e:
                        raise serializers.ValidationError(e)
                    except Exception as e:
                        print(e)
                        raise serializers.ValidationError(f"An error occurred: {str(e)}")
                  
                  for itm in contents:
                    try:
                        Select_content_Package.objects.create(selected_user_package=instance,**itm)
                    except IntegrityError as e:
                        print(e)
                        raise serializers.ValidationError(e)
                    
                
                
                except IntegrityError as e:
                    print(e)
                    raise serializers.ValidationError(e)
            return validated_data
            
        except IntegrityError as e:
            raise serializers.ValidationError(e)
        
class ImageSerializer(serializers.Serializer):
    files = serializers.ListField(child=serializers.ImageField())
    user_name=serializers.CharField()
    gig_id=serializers.IntegerField()
    class Meta:
        model=Gig_Images
        fields=['files','user_name','gig_id']

    def create(self, validated_data):
        try:
            files=validated_data.pop('files',[])
            user_name=validated_data.pop('user_name',None)
            gig_id=validated_data.pop('gig_id',None)
            user_instance=User.objects.get(username=user_name)
            gig_instance=GigData(user=user_instance,id=gig_id)
            images_instac=Gig_Images.objects.filter(gig=gig_instance)
            images_instac.delete()
            
            files_data=[]
            for file in files:
                try:
                    s3 = boto3.client(
                        's3',
                        aws_access_key_id='AKIA2UC27FQCXBZKOAUO',
                        aws_secret_access_key='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',
                        region_name='eu-north-1'
                    )
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    image_key = f"profile_images/{timestamp}_{file.name}".replace(" ","")
                    s3.upload_fileobj(file, 'wishtun', image_key)
                    s3_url = f"https://wishtun.s3.amazonaws.com/{image_key}"
                    # validated_data['profile_image'] = s3_url
                    print(s3_url)
                    images_instacne=Gig_Images.objects.create(gig=gig_instance,Image_url=s3_url)
                    files_data.append(s3_url)
                    

                except ClientError as e:
                    print(f"Error uploading profile image to S3: {e}")
                
            
            
            # print(validated_data)
            
            # print(validated_data)
            return files_data
        except User.DoesNotExist as e:
            raise serializers.ValidationError(e)
        except GigData.DoesNotExist as e:
            raise serializers.ValidationError(e)
        except Exception as e:
            raise serializers.ValidationError(e)
        
        
        