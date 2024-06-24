from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
class Select_content_Package(models.Model):
    selected_user_package = models.ForeignKey('Select_User_Packages', on_delete=models.CASCADE, null=True, related_name='content')
    content_id=models.IntegerField()
    title=models.CharField(max_length=100)
    translated_label=models.CharField(max_length=100)
    edit_type=models.CharField(max_length=100)
    included_modifications=models.CharField(max_length=100)
    active=models.BooleanField()
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'UserPackages_Content' 
    
    
    
    
class Select_User_Packages(models.Model):
   
    gig = models.ForeignKey('GigData', on_delete=models.CASCADE, null=True, related_name='packages')
    duration_unit=models.CharField(max_length=100)
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    duration=models.CharField(max_length=100)
    price=models.CharField(max_length=100)
    is_duration_limit=models.BooleanField()
    is_content=models.BooleanField()
    created_at = models.DateTimeField('created_at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.duration_unit

    class Meta:
        db_table = 'UserPackages' 

class Gig_Category(models.Model):
    gig = models.ForeignKey('GigData', on_delete=models.CASCADE, null=True, related_name='categories')
    category_id = models.CharField(max_length=100)
    sub_category_id = models.CharField(max_length=100)
    service_type = models.BooleanField()
    server_type_id=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_id

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class GigData(models.Model):
    title = models.CharField(max_length=255)
    category = models.ManyToManyField(Gig_Category)
    description = models.TextField()
    status=models.BooleanField(default=False)
    
    # tags = models.ManyToManyField(Tag)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    # delivery_time = models.IntegerField(help_text="Delivery time in days", validators=[MinValueValidator(1)])
    # seller_name = models.CharField(max_length=100)
    # seller_email = models.EmailField()
    # image = models.ImageField(upload_to='gig_images/', null=True, blank=True)
    # featured = models.BooleanField(default=False)
    # active = models.BooleanField(default=True)
    # rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    # reviews_count = models.IntegerField(default=0)
    # views_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

