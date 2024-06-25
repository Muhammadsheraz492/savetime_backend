from django.db import models

# Create your models here.
class Buyer_User(models.Model):
    # _id = djongo_models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    firstname = models.CharField(max_length=100, default='')
    lastname = models.CharField(max_length=100, default='')
    username = models.CharField(max_length=200, unique=True,)
    profile_image=models.CharField(max_length=225,null=True,blank=True)
    email = models.EmailField(unique=True, default='')
    password = models.CharField(max_length=200, default='')
   
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.username
    class Meta:
        db_table = 'Buyer_User'
    