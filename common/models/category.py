from django.db import models

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
    options = models.ManyToManyField(Options, related_name='metadata')
    created_at = models.DateTimeField('created_at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'GigMetaData'

class ServiceType(models.Model):
    subcategory = models.ForeignKey('Subcategory', on_delete=models.CASCADE, null=True, related_name='service_types')
    name = models.CharField(max_length=100)
    description = models.TextField()
    has_nested_gig_metadata = models.BooleanField()
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
    service_type_data = models.ManyToManyField(ServiceType, related_name='subcategories')
    created_at = models.DateTimeField('created_at', auto_now_add=True, null=True)
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
