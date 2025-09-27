from django.contrib import admin
from website.models import Products,authuser
# Register your models here.
admin.site.register(Products)
admin.site.register(authuser)
# class AdminProduct(admin.ModelAdmin):
    # model = Products
    # list_display =('id','name','price','stock')


