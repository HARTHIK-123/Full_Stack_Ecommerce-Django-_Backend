from rest_framework import serializers  
from website.models import Products
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields =['id', 'name', 'description', 'price']