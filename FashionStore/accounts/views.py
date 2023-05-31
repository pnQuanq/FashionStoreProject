
from django.shortcuts import redirect, render
from django.contrib import messages      
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect,HttpResponse

from products.models import *
# Create your views here.
from .models import Cart, CartItems, Profile


def profile(request):
    return render(request ,'accounts/profile.html')

def login_page(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        

        try:
            user_obj = User.objects.filter(username = username)   
        except:
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)
 
        user_obj = authenticate(request , username = username , password= password)

        if user_obj:
            login(request , user_obj)
            return redirect('/')
        else:
            messages.warning(request, 'Username or password does not exist.')
            return HttpResponseRedirect(request.path_info)

    return render(request ,'accounts/login.html')


def register_page(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            user.save()
            login(request, user)
            return redirect('index')
        else:
            messages.warning(request, 'An error occurred during registration.')
    return render(request ,'accounts/register.html', {'form' : form})

def add_to_cart(request , uid):
    variant = request.GET.get('variant')

    product = Product.objects.get(uid = uid)
    user = request.user
    cart ,  _ = Cart.objects.get_or_create(user = user , is_paid = False)

    cart_item = CartItems.objects.create(cart = cart , product = product , )

    if variant:
        variant = request.GET.get('variant')
        size_variant = SizeVariant.objects.get(size_name = variant)
        cart_item.size_variant = size_variant
        cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_cart(request , cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid =cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
def cart(request):
    cart_obj = Cart.objects.get(is_paid = False, user = request.user)
    context = {'cart' : cart}

    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)

        if not coupon_obj.exists():
            messages.warning(request, 'Invalid Coupon.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart_obj.coupon:
            messages.warning(request, 'Coupon already exists.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart_obj.get_cart_total() < coupon_obj[0].minimum_amount:
            messages.warning(request, f'Amount should be greater than {coupon_obj[0].minimum_amount}.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if coupon_obj[0].is_expired:
            messages.warning(request, 'Coupon expired.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



        
        cart_obj.coupon = coupon_obj[0]
        cart_obj.save()
        messages.warning(request, 'Coupon applied.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    context = {'cart' : cart_obj}    

    return render(request , 'accounts/cart.html', context)

def remove_coupon(request, cart_id):
    cart = Cart.objects.get(uid = cart_id)
    cart.coupon = None
    cart.save()
    messages.warning(request, 'Coupon removed.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))