from django.shortcuts import render,redirect
from apps.items .models import Product
from apps.items .forms import  ProductForm
from apps.orders.models import Order
from django.contrib import messages
from django.contrib.auth.decorators import login_required



@login_required
def index(request):
    orders = Order.objects.all().order_by('-created_at')   
    pending_orders_count = orders.filter(status='Pending').count()
    paid_orders_count = orders.filter(status='Paid').count()
    shipped_orders_count = orders.filter(status='Shipped').count()
    done_orders_count = orders.filter(status='Done').count()
    canceled_orders_count = orders.filter(status='Canceled').count()
    
    context = {
        'tittle':'dashboard',
        'orders': orders,
        'pending_orders_count': pending_orders_count,
        'paid_orders_count': paid_orders_count,
        'shipped_orders_count': shipped_orders_count,
        'done_orders_count': done_orders_count,
        'canceled_orders_count': canceled_orders_count,
    }
    return render(request , 'dashboard/daftar_pesanan.html',context)


@login_required
def datasales(request):
    context = {
        'tittle':'data penjualan'
    }
    return render(request, 'dashboard/data_sales.html',context)

@login_required
def productlist(request):
    items = Product.objects.all()
    context = {
        'items':items,
        'tittle':'daftar product'
    }
  
    return render (request, 'dashboard/crud_product.html', context)

@login_required
def addproduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() 
            return redirect('dashboard:productlist')
        else:
            print('terdapat masalah') 
            print(form.errors)  
    else:
        form = ProductForm()
    context = {
        'form': form,
        'tittle':'tambah produk'
    }
    return render(request , 'dashboard/add_product.html',context)

@login_required
def deleteproduct(request,id_product):
    Product.objects.filter(id_product = id_product).delete()
    messages.success(request, "Produk berhasil dihapus!")  
    return redirect('dashboard:productlist')

@login_required
def editproduct(request,id_product):
    obj = Product.objects.get(id_product=id_product)
    if request.method == 'POST':
        form = ProductForm(request.POST or None, instance = obj)
        if form.is_valid():
            form.save()
            return redirect('dashboard:productlist')
        
    else:
        form = ProductForm(instance= obj)
    context={
        'tittle':'edit product',
        'form': form
    }
    return render(request, 'dashboard/edit_product.html', context)

@login_required
def sendorder(request,order_id):
    if request.method == "POST":
        obj = Order.objects.get(order_id= order_id)
        if obj.status == "Paid":
            obj.status = "Shipped"
            obj.save()
        else:
            obj.status = "Paid"
            obj.save()
        return redirect('dashboard:index')
    else:
        return redirect('dashboard:index')