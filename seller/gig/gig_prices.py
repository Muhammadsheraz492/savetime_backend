from django.db import IntegrityError
from rest_framework import serializers
from common.models.gig import Select_User_Packages,GigData
from common.models.category import Subcategory

class UserPackages(serializers.ModelSerializer):

    # name = serializers.CharField(max_length=100
    class Meta:
        model = Select_User_Packages
        fields = ['id','duration_unit','title','description','duration','price']

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
                return serializers.ValidationError("Category Id are not Found")
            gig=GigData.objects.get(id=category_id)
            user_instance=Select_User_Packages.objects.filter(gig=gig)
            user_instance.delete()
            for item in packages:
                try:
                  print(item['price'])
                  is_duration_limit=False
                  is_content=False
                  if item.get('duration_limit') is not None:
                    is_duration_limit = True
                  item['is_duration_limit']=is_duration_limit
                  item['is_content']=is_content
                  
                  Select_User_Packages.objects.create(gig=gig,**item)
                except IntegrityError as e:
                    print(e)
                    raise serializers.ValidationError(e)
            return validated_data
            
        except IntegrityError as e:
            raise serializers.ValidationError(e)
        
        