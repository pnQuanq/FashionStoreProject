from django.shortcuts import render
from products.models import Product

def index(request):

    q = request.GET.get('q')

    context = {'products' : Product.objects.all()}
    return render(request , 'home/index.html' , context)

