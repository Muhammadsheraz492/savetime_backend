from django.db import IntegrityError

from rest_framework import serializers
from common.models.category import *
from common.models.category import Packages
class DurationLimit_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DurationLimit
        fields = ['number']
class DataOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataOptions
        fields = ['value', 'text', 'val']
class ContentSerializer(serializers.ModelSerializer):
    data_options = DataOptionsSerializer(many=True, required=False)
    

    class Meta:
        model = Content
        fields = ['title', 'translated_label', 'edit_type', 'data_options']
class Content_Serializer(serializers.ModelSerializer):
    

    class Meta:
        model = Content
        fields = ['id','title', 'translated_label', 'edit_type', 'data_options']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.data_options:
            data_options_=DataOptions.objects.filter(content=instance.id)
            remove=data.pop('data_options')
            data_options_data=DataOptionsSerializer(data_options_,many=True).data
            data['data_options']=data_options_data
        return data
            



class Packages_serializer(serializers.ModelSerializer):
    duration_limit=serializers.ListField(child=serializers.IntegerField(),required=False)
    content=ContentSerializer(many=True,required=False)
    is_duration_limit=serializers.BooleanField(required=False, read_only=True)
    is_content=serializers.BooleanField(required=False, read_only=True)
    class Meta:
        model = Packages
        fields = ['id', 'duration_limit','duration_unit','content','is_duration_limit','is_content']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.is_duration_limit:
            durationlimit=DurationLimit.objects.filter(package_id=instance.id)
            durationlimit_data=DurationLimit_Serializer(durationlimit,many=True).data
            data['duration_limit']=[int(item['number']) for item in durationlimit_data]
        if instance.is_content:
            content=Content.objects.filter(package=instance.id)
            content_data=Content_Serializer(content,many=True).data
            # print(content_data)
            data['content']=content_data
            
            
        return data
        
    

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Options
        fields = ['id', 'name','title',]
class GigMetaDataSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, required=False)
    class Meta:
        model = GigMetaData
        fields = ['id', 'name','title','description','type','options']

class ServiceTypeSerializer(serializers.ModelSerializer):
    gig_metadata = GigMetaDataSerializer(many=True, required=False)
    packages=Packages_serializer(many=True,required=False,write_only=False)
    has_nested_gig_metadata = serializers.BooleanField(required=False, read_only=True)
    has_gig_price = serializers.BooleanField(required=False, read_only=True)
    class Meta:
        model = ServiceType
        fields = ['id', 'name','description','gig_metadata','has_nested_gig_metadata','has_gig_price','packages']

class SubCategorySerializer(serializers.ModelSerializer):
    # service_type_data = serializers.ListField(required=False)
    service_type_data = ServiceTypeSerializer(many=True, required=False)
    packages=Packages_serializer(many=True,required=False,write_only=False)
    has_nested_gig_metadata = serializers.BooleanField(required=False, read_only=True)
    is_price= serializers.BooleanField(required=False, read_only=True)
    
    service_type = serializers.BooleanField(required=False, read_only=True)
    gig_metadata= GigMetaDataSerializer(many=True, required=False)

    class Meta:
        model = Subcategory
        fields = ['id', 'name','description','service_type_data','has_nested_gig_metadata','service_type','gig_metadata','packages','is_price']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # data.pop('service_type_data')
        # data.pop('packages')
        # print(data)
        if data['service_type']:
            servertype=ServiceType.objects.filter(subcategory=instance.id)
            servertype_serializer=ServiceTypeSerializer(servertype,many=True).data
            data['service_type_data']=servertype_serializer
 
        packages=data.pop('packages',[])
            
  
        return data
    
class CategorySerializer(serializers.ModelSerializer):
    sub_categories=SubCategorySerializer(many=True)
    class Meta:
        model = Category
        fields = ['id','name','email','description','sub_categories']
    def _create_data_options(self,content_instance,data_options):
        for option in data_options:
            try:
                DataOptions.objects.create(content=content_instance,**option)
            except IntegrityError as e:
                raise serializers.ValidationError(e)
    def _create_content(self,package_instance,contents):
        for content in contents:
            try:
                data_options=content.pop('data_options',[])
                is_data_options=bool(data_options)
                content['data_options']=is_data_options
                content_instance=Content.objects.create(package=package_instance,**content)
                if is_data_options:
                    self._create_data_options(content_instance=content_instance,data_options=data_options)
            except IntegrityError as e:
                raise serializers.ValidationError(e)
    def _create_duration(self,package_instance,durations):
        for itm in durations:
            try:
            #   print(x)
               data={}
               data['number']=itm
               DurationLimit.objects.create(package_id=package_instance,**data)
            except IntegrityError as e:
                raise serializers.ValidationError(e)
        
        pass
    def _create_package(self,subcategory_instance,packages):
        # print(packages)
        for package in packages:
            try:
                duration_limit=package.pop('duration_limit',[])
                content=package.pop('content',[])
                is_duration_limit=bool(duration_limit)
                is_content=bool(content)
                package['is_duration_limit']=is_duration_limit
                package['is_content']=is_content
                package_instance=Packages.objects.create(subcategory=subcategory_instance,**package)
                if is_duration_limit:
                    self._create_duration(package_instance=package_instance,durations=duration_limit)
                if is_content:
                    self._create_content(package_instance=package_instance,contents=content)
                
            except IntegrityError as e:
                raise serializers.ValidationError(e)
    def _create_package_with_service_type(self,subcategory_instance,service_type_instance,packages):
        # print(packages)
        for package in packages:
            try:
                duration_limit=package.pop('duration_limit',[])
                content=package.pop('content',[])
                is_duration_limit=bool(duration_limit)
                is_content=bool(content)
                package['is_duration_limit']=is_duration_limit
                package['is_content']=is_content
                package_instance=Packages.objects.create(subcategory=subcategory_instance,servicetype=service_type_instance,**package)
                if is_duration_limit:
                    self._create_duration(package_instance=package_instance,durations=duration_limit)
                if is_content:
                    self._create_content(package_instance=package_instance,contents=content)
                
            except IntegrityError as e:
                raise serializers.ValidationError(e)
                
      
    def _create_options(self,metadata_instance,options):
        for option in options:
            try:
                instance=Options.objects.create(gig_meta_data=metadata_instance,**option)
            except IntegrityError as e:
                raise serializers.ValidationError(e)
    def _create_gigmetadata(self,service_type_instance,metadata):
        for data in metadata:
            try:
                options=data.pop('options',[])
                instance=GigMetaData.objects.create(service_type=service_type_instance,**data)
                self._create_options(metadata_instance=instance,options=options)
            except IntegrityError as e:
                raise serializers.ValidationError(e)
            
    def _create_subcategory_metadata(self,subcategory_instance,metadata):
        for data in metadata:
            try:
                options=data.pop('options',[])
                instance=GigMetaData.objects.create(subcategory=subcategory_instance,**data)
                # self._create_options(metadata_instance=instance,options=options)
            except IntegrityError as e:
                raise serializers.ValidationError(e)
       
            
            
    def _create_servicetype(self,subcategory_instance,servicetypes):
        for servicetype in servicetypes:
            try:
                gig_metadata=servicetype.pop('gig_metadata',[])
                has_nested_gig_metadata=bool(gig_metadata)
                servicetype['has_nested_gig_metadata']=has_nested_gig_metadata
                packages=servicetype.pop('packages',[])
                has_gig_price=bool(packages)
                servicetype['has_gig_price']=has_gig_price
                instance=ServiceType.objects.create(subcategory=subcategory_instance,**servicetype)
                if has_gig_price:
                    self._create_package_with_service_type(subcategory_instance=subcategory_instance,service_type_instance=instance,packages=packages)
                    
                if has_nested_gig_metadata:
                    self._create_gigmetadata(service_type_instance=instance,metadata=gig_metadata)
            except IntegrityError as e:
                raise serializers.ValidationError(e)
    
            
            
            
    def _create_subcategories(self, user_instance, subcategorys):
        for subcategory in subcategorys:
            try:
                service_type_data = subcategory.pop('service_type_data', [])
                gig_metadata = subcategory.pop('gig_metadata', [])
                packages=subcategory.pop('packages',[])
                has_nested_gig_metadata = bool(gig_metadata)
                is_price=bool(packages)
                serive_type = bool(service_type_data)
                subcategory['has_nested_gig_metadata'] = has_nested_gig_metadata
                subcategory['service_type'] = serive_type
                subcategory['is_price']=is_price
                subcategory_instance=Subcategory.objects.create(category=user_instance, **subcategory)  
                if service_type_data:
                    self._create_servicetype(subcategory_instance=subcategory_instance,servicetypes=service_type_data)
                if has_nested_gig_metadata:
                    self._create_subcategory_metadata(subcategory_instance=subcategory_instance,metadata=gig_metadata)
                if is_price:
                    self._create_package(subcategory_instance=subcategory_instance,packages=packages)
              
            except IntegrityError as e:
                    raise serializers.ValidationError(e)
    def create(self, validated_data):
        # print(validated_data)
        # # return {'check':'trw'}
        # try:
        #     subcategorys=validated_data.pop('sub_categories',[])
        #     instance= super().create(validated_data)
        #     # self._create_devices(instance,subcategorys)
        #     return instance
        # except IntegrityError as e:
        #     raise serializers.ValidationError(e)
         
        subcategories_data = validated_data.pop('sub_categories', [])
        try:
            # Check if category with the same name already exists
            instance = Category.objects.get(name=validated_data['name'])
            print(instance)
            raise serializers.ValidationError({'success': False, 'message': 'Category with this name already exists.'})
        except Category.DoesNotExist:
            instance = Category.objects.create(**validated_data)
            self._create_subcategories(instance, subcategories_data)
            return instance
        except IntegrityError as e:
            raise serializers.ValidationError(str(e))
        

    def to_representation(self, instance):
        representation = super().to_representation(instance)
    #     # # representation.pop('devices')
        subcategory = Subcategory.objects.filter(category=instance.id)
    #     # devices_representation = AdminDeviceSerializer(user_devices, many=True).data
        subcategory_representation=SubCategorySerializer(subcategory,many=True).data
    #     representation['sub_categories'] = subcategory_representation
    #     # subcategory=Subcategory.objects.filter(category_id=instance.id)
    #     # subcategory_representation=SubCategorySerializer(subcategory,many=True).data
        representation['sub_categories']=subcategory_representation
        
        
        return representation
    