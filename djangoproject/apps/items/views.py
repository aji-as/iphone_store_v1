from django.shortcuts import render , redirect
from django.db.models import Q
from .models import Product

# Create your views here.
def index(request):
    products = Product.objects.all()

    # Handle search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
        
    print(products)
    
    return render(request, 'items/index.html', {
        'products': products,
        'search_query': search_query
    })
    
def detailproduct(request, id_product):
    product = Product.objects.get(id_product = id_product)
    related_products = Product.objects.filter(
        Q(name__icontains=product.name.split()[0]) | 
        Q(ram=product.ram) | 
        Q(memory=product.memory)
    ).exclude(id_product=product.id_product)[:8]
    
    context = {
        'product': product,
        'products': related_products
    }
    return render(request, 'items/detail_product.html', context)
   
   
def daftarproduct(request):
    products = Product.objects.all()  # semua data dulu
     # inisialisasi default
    search_query = ''
    if request.method == 'POST':
        search_query = request.POST.get('search', '').strip()
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

    return render(request, 'items/daftar_produk.html', {
        'products': products,
        'search_query': search_query,
    })
        
