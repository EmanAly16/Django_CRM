from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
	user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
	name=models.CharField(max_length = 200,null=True)
	phone=models.CharField(max_length = 200,null=True)
	email=models.CharField(max_length = 200,null=True)
	profile_pic=models.ImageField(default="profile.png",null=True,blank=True)
	data_created=models.DateTimeField(auto_now_add=True)

    #to return the name as the string visable in the table rather than object1 
	def __str__(self):
		return self.name 
	#"""docstring for ClassName"""
	#def __init__(self, arg):
	#	super(ClassName, self).__init__()
	#	self.arg = arg

class Tag(models.Model):
    name=models.CharField(max_length = 200,null=True)
  
    def __str__(self):
        return self.name 
class Product(models.Model):
	CATEGORY=(
		('Indoor','Indoor'),
		('Out Door','Out Door'),
		)
	name=models.CharField(max_length = 200,null=True)
	price=models.FloatField(null=True)
	category=models.CharField(max_length = 200,null=True,choices=CATEGORY)
	description=models.CharField(max_length = 200,null=True,blank=True)
	data_created=models.DateTimeField(auto_now_add=True)
	#to make a many to many relationship
	tags=models.ManyToManyField(Tag)
	def __str__(self):
		return self.name 

class Order(models.Model):
	STATUS=(
		('Pending','Pending'),
		('Out for delivery','Out for delivery'),
		('Delivery','Delivery'),
		)
	# to make ralation with them
	customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
	Product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
	data_created=models.DateTimeField(auto_now_add=True)
	status=models.CharField(max_length = 200, null=True, choices=STATUS)
	note=models.CharField(max_length = 1000, null=True)
	def __str__(self):
		return self.Product.name	