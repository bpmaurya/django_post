from django.shortcuts import render,redirect
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product

@login_required(login_url='/login')
def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        weight = request.POST.get('weight')
        product = Product(name=name, price=price, weight=weight)
        product.save()
        print(name, price, weight)
        return redirect("product_list/")
    return render(request, 'product.html')


@login_required(login_url='/login')
def ProductList(request):
    myProduct = Product.objects.all()

    return render(request, 'productList.html',{'myproduct': myProduct})

