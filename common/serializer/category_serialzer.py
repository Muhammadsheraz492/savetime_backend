from django.db import IntegrityError

from rest_framework import serializers
from common.models.category import *
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
    has_nested_gig_metadata = serializers.BooleanField(required=False, read_only=True)
    class Meta:
        model = ServiceType
        fields = ['id', 'name','description','gig_metadata','has_nested_gig_metadata']

class SubCategorySerializer(serializers.ModelSerializer):
    # service_type_data = serializers.ListField(required=False)
    service_type_data = ServiceTypeSerializer(many=True, required=False)
    has_nested_gig_metadata = serializers.BooleanField(required=False, read_only=True)
    service_type = serializers.BooleanField(required=False, read_only=True)
    gig_metadata= GigMetaDataSerializer(many=True, required=False)

    class Meta:
        model = Subcategory
        fields = ['id', 'name','description','service_type_data','has_nested_gig_metadata','service_type','gig_metadata']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('service_type_data')
        # print(data)
        if data['service_type']:
            servertype=ServiceType.objects.filter(subcategory=instance)
            servertype_serializer=ServiceTypeSerializer(servertype,many=True).data
            data['service_type_data']=servertype_serializer
            
            
            # data.pop("")
        return data
    
class CategorySerializer(serializers.ModelSerializer):
    sub_categories=SubCategorySerializer(many=True)
    class Meta:
        model = Category
        fields = ['id','name','email','description','sub_categories']
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
                self._create_options(metadata_instance=instance,options=options)
            except IntegrityError as e:
                raise serializers.ValidationError(e)
       
            
            
    def _create_servicetype(self,subcategory_instance,servicetypes):
        for servicetype in servicetypes:
            try:
                gig_metadata=servicetype.pop('gig_metadata',[])
                has_nested_gig_metadata=bool(gig_metadata)
                servicetype['has_nested_gig_metadata']=has_nested_gig_metadata
                instance=ServiceType.objects.create(subcategory=subcategory_instance,**servicetype)
                if has_nested_gig_metadata:
                    self._create_gigmetadata(service_type_instance=instance,metadata=gig_metadata)
            except IntegrityError as e:
                raise serializers.ValidationError(e)
    
            
            
            
    def _create_subcategories(self, user_instance, subcategorys):
        for subcategory in subcategorys:
            try:
                service_type_data = subcategory.pop('service_type_data', [])
                gig_metadata = subcategory.pop('gig_metadata', [])
                has_nested_gig_metadata = bool(gig_metadata)
                serive_type = bool(service_type_data)
                subcategory['has_nested_gig_metadata'] = has_nested_gig_metadata
                subcategory['service_type'] = serive_type
                subcategory_instance=Subcategory.objects.create(category=user_instance, **subcategory)  
                if service_type_data:
                    self._create_servicetype(subcategory_instance=subcategory_instance,servicetypes=service_type_data)
                if has_nested_gig_metadata:
                    self._create_subcategory_metadata(subcategory_instance=subcategory_instance,metadata=gig_metadata)
              
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
        subcategory = Subcategory.objects.filter(category=instance.id)
        # devices_representation = AdminDeviceSerializer(user_devices, many=True).data
        subcategory_representation=SubCategorySerializer(subcategory,many=True).data
        representation['sub_categories'] = subcategory_representation
        # subcategory=Subcategory.objects.filter(category_id=instance.id)
        # subcategory_representation=SubCategorySerializer(subcategory,many=True).data
        # representation['sub_categories']=subcategory_representation
        
        
        return representation
    