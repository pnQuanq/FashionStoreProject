
from django.shortcuts import redirect, render
from django.contrib import messages      
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from .forms import ProfileForm
from django.http import HttpResponseRedirect,HttpResponse

from products.models import *
# Create your views here.
from .models import Cart, CartItems, Profile
from django.contrib.auth.decorators import login_required 

@login_required(login_url='login')
def editProfile(request):
    user = request.user
    p_form = ProfileForm(instance=user)

    context = {'p_form': p_form}
    return render(request ,'accounts/editProfile.html', context)

@login_required(login_url='login')
def profile(request):
    return render(request ,'accounts/profile.html')

def login_page(request):
    
    if request.method == 'POST':
        username = request.POST.get('userName')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = username)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)



        user_obj = authenticate(username = username , password= password)
        if user_obj:
            login(request , user_obj)
            return redirect('/')

        

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)

    return render(request ,'accounts/login.html')

def register_page(request):
    if request.method=='POST':
        user_name = request.POST.get('userName')
        email = request.POST.get('email')
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        password = request.POST.get('password')
        re_pass = request.POST.get('rePassword')

        if password != re_pass:
            messages.warning(request, 'Coupon already exists.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            user = User.objects.create_user(first_name = firstName , last_name= lastName , email = email , username = user_name)
            user.set_password(password)
            user.save()
            return redirect('index')
    return render(request ,'accounts/register.html')

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