from django.shortcuts import render
from products.models import Product, Category

def index(request):

    if 'que' in request.GET:
        que = request.GET['que']
        products = Product.objects.filter(product_name__icontains=que)
    else:
        products = Product.objects.all()

    categories = Category.objects.all()
    
    if 'q' in request.GET:
        q = request.GET['q']
        products = Product.objects.filter(product_name__icontains=q)
        

    context = {'products' : products, 'categories' : categories}
    return render(request , 'home/index.html' , context)

