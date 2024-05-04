from django.db import models
# from django.contrib.auth.models import User
from USERS.models import CustomUser
import secrets

# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.name

class ShoeBrand (models.Model):
    name = models.CharField(max_length=200,default=None,blank=True)

    def __str__(self):
        return self.name
    
class SizeAvailable (models.Model):
    size = models.IntegerField()
    class Meta:
        ordering = ['size']

    def __str__(self):
        return str(self.size)
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    brand = models.ForeignKey(ShoeBrand, on_delete=models.CASCADE, default="", null=True,blank=True)
    size_available = models.ManyToManyField(SizeAvailable,blank=True,null=True,default=None)
    price = models.FloatField()
    old_price = models.FloatField(blank=True,default=0.0)

    image = models.ImageField(upload_to='product_images/')
    image_2 = models.ImageField(upload_to='product_images/', default=None,blank=True,null=True)
    image_3 = models.ImageField(upload_to='product_images/', default=None,blank=True,null=True)

    out_of_stock = models.BooleanField(default=False)
    
    # GET CATEGORIES LATER
    category = models.ManyToManyField(ProductCategory)
    
    quantity_available = models.PositiveIntegerField()

    def __str__(self):
        return (self.name)
    

    


class BasePopup(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True)

##About to implement payment APIs in the views