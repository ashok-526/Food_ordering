from django.db.models import *
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
# Create your views here.
import uuid

def login_page(request):

    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        if not User.objects.filter(username = username).exists():

            messages.error(request, "Invalid username!")

            return redirect('/login/')
                
        user = authenticate(username =username , password = password)

        if user is None:
            messages.error(request, "Invalid PASSWORD!")
            return redirect('/login/')

        else:
            login(request , user)
            return redirect('/')

    return render(request , 'login.html')


def register(request):

    if request.method == 'POST':

        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.filter(username=username)

        if user.exists():
            messages.error(request, "Username already exists!!")

            return redirect('/register')

        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            

            )


        user.set_password(password)
        user.save()
        messages.info(request, "Account Created Successfully")

        return redirect('/login/')


    return render(request , 'register.html')

@login_required(login_url="/login/")
def order_home(request):
	pizzas = Pizza.objects.all()
	context = {'pizzaa':pizzas}
	return render(request , 'order.html',context)


def add_card(request , pizza_uid):

	user = request.user ## to know who is user
	pizza_obj = Pizza.objects.get(uid = pizza_uid)
	cart , _ = Cart.objects.get_or_create(user = user , is_paid=False)
  # Extract the actual Cart instance from the tuple

	cart_items = CartItem.objects.create(
    cart_reference=cart,  # Use the extracted Cart instance
    pizza_reference=pizza_obj
)


	return redirect("/")



@login_required(login_url="/login/")
def cart(request):
    cart = Cart.objects.get(is_paid=False, user=request.user)
    total_price = CartItem.objects.filter(cart_reference=cart).aggregate(Sum('pizza_reference__price'))['pizza_reference__price__sum']

    context = {'carts': cart, 'total': total_price, 'order': cart}  # Include the 'order' object in the context
    return render(request, 'cart.html', context)


def remove_item(request , remove_item):
    try:

        CartItem.objects.get(uid=remove_item).delete()

        

    except Exception as e:
        print(e)


    return redirect("/cart")


from django.db.models import Sum, F, ExpressionWrapper, FloatField

@login_required(login_url="/login/")
def dashboard(request):
    dash_boards = Cart.objects.filter(is_paid=False, user=request.user)

    for dashboard in dash_boards:
        # Calculate the total price by summing the product of pizza price and quantity
        total_price = dashboard.food_items.annotate(
            item_total=ExpressionWrapper(F('pizza_reference__price') * F('quantity'), output_field=FloatField())
        ).aggregate(total=Sum('item_total'))['total']
        dashboard.total_price = total_price if total_price else 0  # Set to 0 if total_price is None

    context = {'dash_boards': dash_boards}
    return render(request, 'dashboard.html', context)

import requests as req



def payment(request, *args, **kwargs):
    # Get the cart and calculate total
    cart = Cart.objects.get(is_paid=False, user=request.user)
    total = CartItem.objects.filter(cart_reference=cart).aggregate(Sum('pizza_reference__price'))['pizza_reference__price__sum']

    # Generate a UUID
    uid = uuid.uuid4()
    
    # Pass total and order to the template context
    context = {'pay_total': total, 'uid': uid}

    url = "https://uat.esewa.com.np/epay/transrec"
    d = {
        'amt': total,
        'scd': 'EPAYTEST',
        'rid': request.GET.get('refid'),
        'pid': uid
    }
    
    resp = req.post(url, d)
    
    if resp.status_code == 200 and resp.text == 'success':
        # Perform the following actions within a transaction
        with transaction.atomic():
            # Add cart items to the cart
            # (Assuming you have a method to add items to the cart)
            # cart.add_items(...) 
            
            # Mark the cart as paid and save it
           if not cart.is_paid:
                cart.is_paid = True
                cart.esewa = request.GET.get('oid')
                cart.save()


        return redirect("/dashboard")
    
    return render(request, 'payment.html', context)
