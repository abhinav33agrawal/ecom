from django.contrib import admin
from shop import models

class AdminProduct(admin.ModelAdmin):
    list_display = ['name','price','category']

class AdminCategory(admin.ModelAdmin):
    list_display = ['name']
# Register your models here.
admin.site.register(models.Product,AdminProduct)
admin.site.register(models.Category,AdminCategory)
admin.site.register(models.Customer)
admin.site.register(models.Order)
admin.site.register(models.ContactUs)