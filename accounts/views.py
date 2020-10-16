from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import *
from .forms import OrderForm,CreateUserForm,CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
# Create your views here.

@unauthenticated_user
def registerPage(request):

	form=CreateUserForm()
	if request.method == 'POST':
		form=CreateUserForm(request.POST)
		if form.is_valid():
			user =form.save()
			#to represent a flash massege when user are created
			username =form.cleaned_data.get('username')
			
			messages.success(request,'Account was created for '+username)
			return redirect('login')

	context={'form':form}
	return render(request,'accounts/register.html',context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username= request.POST.get('username')
		password= request.POST.get('password')
		user =authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('home')
		else:
			messages.info(request,'Username or Password is incorrect')

	context={}
	return render(request,'accounts/login.html',context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
	orders=Order.objects.all()
	customers=Customer.objects.all()
	total_customers=customers.count()
	total_orders=orders.count()
	delivered=orders.filter(status='Delivery').count()
	pending=orders.filter(status='Pending').count()
	context={'orders':orders,'customers':customers,'total_customers':total_customers,
	'total_orders':total_orders,'delivered':delivered,'pending':pending}
	return render(request,'accounts/dashboard.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivery').count()
	pending = orders.filter(status='Pending').count()

	print('ORDERS:', orders)

	context = {'orders':orders, 'total_orders':total_orders,
	'delivered':delivered,'pending':pending}
	return render(request, 'accounts/user.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	# to pass the value to the prodect tamplet page
	products=Product.objects.all()
	# the first value before : it's the name we want to use in the product page to print item
	return render(request,'accounts/products.html',{'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
	customer=Customer.objects.get(id=pk_test)
	orders=customer.order_set.all()
	order_count=orders.count()
	myFilter=OrderFilter(request.GET,queryset=orders)
	orders=myFilter.qs
	context={'customer':customer,'orders':orders,'order_count':order_count,'myFilter':myFilter}
	# to go to templates then open folder account then the customer page
	return render(request,'accounts/customer.html',context)
   #it will return page with text Customer page
   #return HttpResponse('Customer page')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
	#take parent modele and child modele then which field to allow
	OrderFormSet=inlineformset_factory(Customer,Order,fields=('Product','status'),extra=10)
	customer=Customer.objects.get(id=pk)
	formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form=OrderForm(initial={'customer':customer})
	if request.method=='POST':
		#print('Printing POST: ',request.POST)
		#form=OrderForm(request.POST)
		formset=OrderFormSet(request.POST,instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')


	context={'formset':formset}
	return  render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
	order=Order.objects.get(id=pk)
	#instance to fill up the form when try to update item
	form=OrderForm(instance=order)
	if request.method=='POST':
		# instance=order becuse we did not need to create new item we want to update spacific item
		form=OrderForm(request.POST,instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context={'form':form}
	return  render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
	order=Order.objects.get(id=pk)
	if request.method=='POST':
		order.delete()
		return redirect('/')

	context={'item':order}
	return  render(request,'accounts/delete.html',context)


