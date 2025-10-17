from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import OrderForm
from apps.items.models import Product


def index(request, id_product):
    product = get_object_or_404(Product, id_product=id_product)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, product=product)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.total_price = product.price * order.quantity
            
            # Check if quantity is available
            if order.quantity > product.stock:
                messages.error(request, f'Maaf, stok hanya tersedia {product.stock} unit')
            else:
                order.save()
                messages.success(request, f'Pesanan berhasil dibuat! Total: Rp{order.total_price:,.0f}')
                return redirect('items:index')
    else:
        form = OrderForm(product=product)

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'orders/index.html', context)


def cekpesanan(request):
    from .models import Order
    
    # Get all orders or filter based on request parameters
    orders = Order.objects.all().select_related('product').order_by('-created_at')
    
    # Handle search query
    search_query = request.GET.get('search', '')
    if search_query:
        orders = orders.filter(order_id__icontains=search_query)
    
    context = {
        'orders': orders,
        'search_query': search_query
    }
    return render(request, 'orders/daftar_order.html', context)