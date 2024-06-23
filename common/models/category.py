from django.db import models
class DataOptions(models.Model):
    content=models.ForeignKey('content', on_delete=models.CASCADE, null=True, related_name='foreign_key_of_packages')
    value=models.CharField(max_length=100)
    text=models.CharField(max_length=100)
    val=models.CharField(max_length=100)
    created_at = models.DateTimeField('created_at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.text  

    class Meta:
        db_table = 'data_options'
class Content(models.Model):
    package=models.ForeignKey('Packages', on_delete=models.CASCADE, null=True, related_name='foreign_key_of_content')
    title=models.CharField(max_length=100)
    translated_label=models.CharField(max_length=100)
    edit_type=models.CharField(max_length=100)
    data_options=models.BooleanField()
    created_at = models.DateTimeField('created_at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title  # Adjust based on what makes sense for your application

    class Meta:
        db_table = 'content'
class DurationLimit(models.Model):
    package_id=models.ForeignKey('Packages', on_delete=models.CASCADE, null=True, related_name='foreign_key_of_packages')
    number=models.CharField(max_length=100)
    created_at = models.DateTimeField('created_at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.number  

    class Meta:
        db_table = 'duration_limit'
    
class Packages(models.Model):
   
    subcategory = models.ForeignKey('Subcategory', on_delete=models.CASCADE, null=True, related_name='packages')
    servicetype = models.ForeignKey('ServiceType', on_delete=models.CASCADE, null=True, related_name='service_types')
    duration_unit=models.CharField(max_length=100)
    is_duration_limit=models.BooleanField()
    is_content=models.BooleanField()
    # duration_limit=models.ManyToManyField(DurationLimit, related_name='durations')
    # gig_meta_data = models.ForeignKey('GigMetaData', on_delete=models.CASCADE, null=True, related_name='related_options')
    # title = models.CharField(max_length=100)
    created_at = models.DateTimeField('created_at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.duration_unit

    class Meta:
        db_table = 'Packages'

class Options(models.Model):
    gig_meta_data = models.ForeignKey('GigMetaData', on_delete=models.CASCADE, null=True, related_name='related_options')
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField('created_at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Options'

class GigMetaData(models.Model):
    subcategory = models.ForeignKey('Subcategory', on_delete=models.CASCADE, null=True, related_name='metadata')
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    service_type = models.ForeignKey('ServiceType', on_delete=models.CASCADE, null=True, related_name='metadata')
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField('created_at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'GigMetaData'

class ServiceType(models.Model):
    subcategory = models.ForeignKey('Subcategory', on_delete=models.CASCADE, null=True, related_name='service_types')
    # packages_id= models.ManyToManyField(Packages, related_name='subcategories')
    name = models.CharField(max_length=100)
    description = models.TextField()
    has_nested_gig_metadata = models.BooleanField()
    has_gig_price = models.BooleanField()
    created_at = models.DateTimeField('created_at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ServiceType'

class Subcategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, related_name='related_subcategories')
    name = models.CharField(max_length=100)
    description = models.TextField()
    has_nested_gig_metadata = models.BooleanField()
    service_type = models.BooleanField()
    is_price=models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Subcategory'

class Category(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    description = models.TextField()
    sub_categories = models.ManyToManyField(Subcategory, related_name='categories')
    created_at = models.DateTimeField('created_at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Category'
