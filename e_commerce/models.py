import django.db.models as model
from django.contrib.auth.models import AbstractUser

class authuser(AbstractUser):   # <-- Check the exact spelling/capitalization
    # any extra fields
    pass

class Products(model.Model):
    #ID field is auto-created by Django as primary key
    name = model.CharField(max_length=250)
    description =  model.TextField()
    price = model.DecimalField(max_digits=10,decimal_places=2)

