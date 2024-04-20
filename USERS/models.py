import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    id =  models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=100,blank=True,null=True)
    last_name = models.CharField(max_length=100,blank=True,null=True)
    date_of_birth = models.DateField(blank=True,null=True)
    username = models.CharField(max_length = 200, unique=True,null=True)
    email = models.EmailField(unique=True)
    phone_number = models.IntegerField(blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    country = models.CharField(max_length=200, blank=True,null=True)


    def __str__(self):
        return (self.email)
    

class SubscribedUsers(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

