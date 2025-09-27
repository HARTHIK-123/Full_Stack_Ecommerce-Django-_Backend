from django.contrib import admin
from website.models import Products,Authuser
# Register your models here.
admin.site.register(Products)
admin.site.register(Authuser)
# class AdminProduct(admin.ModelAdmin):
    # model = Products
    # list_display =('id','name','price','stock')


