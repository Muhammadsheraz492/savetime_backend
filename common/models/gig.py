from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Gig_Category(models.Model):
    gig_id = models.ForeignKey('Gig', on_delete=models.CASCADE, null=True, related_name='related_gigs')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Gig(models.Model):
    title = models.CharField(max_length=255)
    category = models.ManyToManyField(Gig_Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_time = models.IntegerField(help_text="Delivery time in days")
    seller_name = models.CharField(max_length=100)
    seller_email = models.EmailField()
    image = models.ImageField(upload_to='gig_images/', null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    reviews_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title
