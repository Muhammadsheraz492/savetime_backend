import logging
from django.db import models
from djongo import models as djongo_models
from bson import ObjectId
from django.utils import timezone
class Subcategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, related_name='subcategories')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField('created_At', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'Sub_Category'

class Category(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    sub_categories = models.ManyToManyField(Subcategory, related_name='categories')
    created_at = models.DateTimeField('created_At', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'Category'
