import django.db.models as model
from django.contrib.auth.models import AbstractUser


class Products(model.Model):
    #ID field is auto-created by Django as primary key
    name = model.CharField(max_length=250)
    description =  model.TextField()
    price = model.DecimalField(max_digits=10,decimal_places=2)
    # stock = model.IntegerField()

    def __str__(self):
        return self.name
    
class Authuser(AbstractUser):
    # inherts all fields of AbstractUser
    email = model.EmailField(unique=True)  # make email unique
    usename = model.CharField(max_length=150, unique=False)  # make username non-unique
    # REQUIRED_FIELDS = ['email','username']  # remove email from REQUIRED_FIELDS
    user_permissions = None  # remove user_permissions field
    groups = None  # remove groups field
    first_name = None  # remove first_name field
    last_name = None  # remove last_name field

    def __str__(self):
        return self.email


