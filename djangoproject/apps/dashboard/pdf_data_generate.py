import pandas as pd
from django.http import HttpResponse
from django.db.models import Sum
from apps.orders.models import Order
from apps.items.models import Product
from io import BytesIO


def export_full_sales_report_excel(request=None):
    """
    Membuat laporan lengkap penjualan dan produk ke dalam file Excel (XLSX)
    dengan dua sheet: Produk dan Order.
    """
    # === BAGIAN 1: DATA PRODUK ===
    products = Product.objects.all().values(
        'id_product', 'name', 'price', 'stock', 'sold', 'ram', 'memory', 'color'
    )

    df_products = pd.DataFrame(list(products))

    if not df_products.empty:
        df_products['Total Pendapatan'] = df_products['price'] * df_products['sold']
        df_products.rename(columns={
            'id_product': 'ID Produk',
            'name': 'Nama Produk',
            'price': 'Harga (Rp)',
            'stock': 'Stok Tersisa',
            'sold': 'Terjual',
            'ram': 'RAM',
            'memory': 'Memori',
            'color': 'Warna',
            'Total Pendapatan': 'Total Pendapatan (Rp)',
        }, inplace=True)
    else:
        df_products = pd.DataFrame(columns=[
            "ID Produk", "Nama Produk", "Harga (Rp)", "Stok Tersisa",
            "Terjual", "RAM", "Memori", "Warna", "Total Pendapatan (Rp)"
        ])

    # === BAGIAN 2: DATA ORDER ===
    orders = Order.objects.select_related('product').all().values(
        'order_id',
        'product__name',
        'buyer_name',
        'buyer_gender',
        'buyer_age',
        'quantity',
        'total_price',
        'status',
        'city',
        'region',
        'created_at'
    )

    df_orders = pd.DataFrame(list(orders))

    if not df_orders.empty:
        df_orders.rename(columns={
            'order_id': 'ID Order',
            'product__name': 'Produk',
            'buyer_name': 'Nama Pembeli',
            'buyer_gender': 'Gender',
            'buyer_age': 'Umur',
            'quantity': 'Jumlah',
            'total_price': 'Total Harga (Rp)',
            'status': 'Status',
            'city': 'Kota',
            'region': 'Wilayah',
            'created_at': 'Tanggal Pesanan'
        }, inplace=True)

        df_orders['Tanggal Pesanan'] = pd.to_datetime(df_orders['Tanggal Pesanan']).dt.strftime('%d-%m-%Y')
    else:
        df_orders = pd.DataFrame(columns=[
            "ID Order", "Produk", "Nama Pembeli", "Gender", "Umur", "Jumlah",
            "Total Harga (Rp)", "Status", "Kota", "Wilayah", "Tanggal Pesanan"
        ])

    # === Total Pendapatan ===
    total_income = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0
    summary_df = pd.DataFrame({
        "Keterangan": ["Total Pendapatan"],
        "Nilai (Rp)": [total_income]
    })

    # === BUAT FILE EXCEL DALAM MEMORY ===
    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_products.to_excel(writer, sheet_name='Ringkasan Produk', index=False)
        df_orders.to_excel(writer, sheet_name='Detail Pesanan', index=False)
        summary_df.to_excel(writer, sheet_name='Ringkasan Total', index=False)

    buffer.seek(0)

    # === KIRIM FILE KE BROWSER ===
    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="laporan_penjualan.xlsx"'

    return response
