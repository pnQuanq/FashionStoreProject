from django.shortcuts import render
from products.models import Product

def index(request):

    q = request.GET.get('q')

    if 'que' in request.GET:
        que = request.GET['que']
        products = Product.objects.filter(product_name__icontains=que)
    else:
        products = Product.objects.all()
    context = {'products' : products}
    return render(request , 'home/index.html' , context)

