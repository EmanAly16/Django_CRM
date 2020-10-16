from django.contrib import admin

# Register your models here.
#to view the customer table in admin page
# * to import all medels
from .models import *
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)