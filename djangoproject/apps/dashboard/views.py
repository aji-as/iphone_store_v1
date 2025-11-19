from django.shortcuts import render,redirect
from apps.items .models import Product
from apps.items .forms import  ProductForm
from apps.orders.models import Order
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from.ai import predictions
from . pdf_data_generate import export_full_sales_report_excel




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
    total_products = Product.objects.count()
    total_sales = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_sold = Order.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0

    # 2️⃣ Penjualan per produk
    product_sales = (
        Order.objects.values('product__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:10]
    )

    # 3️⃣ Kota dengan penjualan iPhone terbanyak
    iphone_sales_by_city = (
        Order.objects.filter(product__name__icontains='iphone')
        .values('city')
        .annotate(total=Sum('quantity'))
        .order_by('-total')
    )

    # 4️⃣ Gender dan umur pembeli iPhone
    gender_sales = (
        Order.objects.filter(product__name__icontains='iphone')
        .values('buyer_gender')
        .annotate(total=Sum('quantity'))
    )

    age_sales = (
        Order.objects.filter(product__name__icontains='iphone')
        .values('buyer_age')
        .annotate(total=Sum('quantity'))
        .order_by('buyer_age')
    )
    
    
    #refresh predictions
    if request.method == 'POST':
        prediksi = predictions(Order)

        # pastikan hasilnya berupa dict
        import json
        if isinstance(prediksi, str):
            try:
                prediksi = json.loads(prediksi)
                print(prediksi)
            except json.JSONDecodeError:
                prediksi = {
                    "prediksi_tren": "Tidak dapat membaca hasil prediksi.",
                    "produk_populer": [],
                    "saran_admin": "Periksa kembali format JSON dari Gemini."
                }

        prediksi_tren = prediksi.get('prediksi_tren')
        produk_populer = prediksi.get('produk_populer')
        saran_admin = prediksi.get('saran_admin')
    else:
        prediksi_tren = None
        produk_populer = None
        saran_admin = None

    

    context = {
        "prediksi_tren":prediksi_tren,
        "produk_populer":produk_populer,
        "saran_admin" :saran_admin,
        "title": "Dashboard Penjualan",
        "total_sold": total_sold,
        "total_products": total_products,
        "total_sales": total_sales,

        # Data untuk grafik Chart.js
        "product_labels": [x['product__name'] for x in product_sales],
        "product_values": [x['total_sold'] for x in product_sales],
        
        "city_labels": [x['city'] for x in iphone_sales_by_city],
        "city_values": [x['total'] for x in iphone_sales_by_city],

        "gender_labels": [x['buyer_gender'] for x in gender_sales],
        "gender_values": [x['total'] for x in gender_sales],

        "age_labels": [x['buyer_age'] for x in age_sales],
        "age_values": [x['total'] for x in age_sales],
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
    
    
@login_required
def export_to_pdf(request):
    response =export_full_sales_report_excel(request)
    return response
    
