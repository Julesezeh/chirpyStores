from django.db import models
# from django.contrib.auth.models import User
from USERS.models import CustomUser
import secrets

# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    old_price = models.FloatField(blank=True,default=0.0)

    image = models.ImageField(upload_to='product_images/')
    out_of_stock = models.BooleanField(default=False)
    
    # GET CATEGORIES LATER
    category = models.ManyToManyField(ProductCategory)
    
    quantity_available = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    

    


class BasePopup(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True)

##About to implement payment APIs in the views