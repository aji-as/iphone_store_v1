import os
from django.db.models import Sum
from dotenv import load_dotenv
from google import genai


load_dotenv() 


def predictions(order):
    try:
        # Ambil data penjualan
        total_sales = order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
        recent_orders = list(order.objects.order_by('-id')[:20].values('product__name', 'quantity', 'total_price'))

        # Prompt untuk Gemini
        prompt = f"""
            Kamu adalah analis penjualan profesional.

            Berdasarkan data penjualan berikut:
            Total penjualan: {total_sales}
            Data pesanan terbaru: {recent_orders}

            Tugas kamu:
            1. Prediksi tren penjualan minggu depan (naik/turun/stabil) dan alasan singkatnya.
            2. Sebutkan 3 produk paling populer dari data di atas.
            3. Berikan saran singkat untuk admin toko.

            Jawablah **hanya** dalam format JSON valid, tanpa teks tambahan, tanpa tanda ```json```, tanpa penjelasan di luar JSON.

            Contoh format yang harus kamu ikuti:
            {{
            "prediksi_tren": "Naik karena permintaan meningkat menjelang akhir bulan.",
            "produk_populer": ["iPhone 15", "Samsung Galaxy S24", "Xiaomi Redmi 13"],
            "saran_admin": "Perbanyak stok produk populer dan promosikan lewat media sosial."
            }}
    """

        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        print("API Key:", os.getenv("GOOGLE_API_KEY"))
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        ai_result = response.text
        
    except Exception as e:
        print("Error koneksi ke Gemini:", e)
        return {
            "prediksi_tren": "Tidak tersedia (koneksi gagal)",
            "produk_populer": [],
            "saran_admin": "Periksa koneksi internet atau API Gemini."
        }

    

    return  ai_result





# import os
# from django.db.models import Sum
# from dotenv import load_dotenv
# from google import genai
# from django.utils import timezone
# from datetime import timedelta
# load_dotenv() 


# def predictions(order):
#     try:
#         # Ambil total penjualan
#         total_sales = order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0

#         # Ambil tanggal 30 hari lalu
#         thirty_days_ago = timezone.now() - timedelta(days=30)

#         recent_orders = list(
#             order.objects.filter(created_at__gte=thirty_days_ago)
#             .order_by('-created_at')
#             .values(
#                 'product__name',
#                 'quantity',
#                 'total_price',
#                 'product__stock'
#             )
#         )

#         # Prompt baru (versi profesional & sesuai prediksi yang dirancang)
#         prompt = f"""
#         Kamu adalah analis penjualan senior yang sangat berpengalaman.

#         Berikut adalah data penjualan:
#         Total penjualan: {total_sales}
#         Data order terbaru (max 30): {recent_orders}

#         Buatkan prediksi penjualan profesional yang terdiri dari:
        
#         1. **sales_forecast**
#            - Prediksi penjualan 7 hari ke depan.
#            - Prediksi penjualan 30 hari ke depan.
#            - Status tren: naik / turun / stabil  
#            - Alasan tren.

#         2. **product_demand**
#            - 3 produk dengan permintaan tertinggi.
#            - 3 produk yang permintaannya menurun.
        
#         3. **inventory_forecast**
#            - Produk yang diprediksi akan habis stok (beserta estimasi hari).
#            - Produk yang aman.
        
#         4. **profit_forecast**
#            - Perkiraan profit 30 hari.
#            - Margin diprediksi naik/turun/stabil.
#            - Faktor yang memengaruhi margin.

#         Jawab **hanya** dalam format JSON valid, TANPA teks tambahan apa pun.

#         Format yang wajib diikuti:
#         {{
#             "sales_forecast": {{
#                 "prediksi_7_hari": "....",
#                 "prediksi_30_hari": "....",
#                 "tren": "naik/turun/stabil",
#                 "alasan": "...."
#             }},
#             "product_demand": {{
#                 "produk_tertinggi": ["...", "...", "..."],
#                 "produk_menurun": ["...", "...", "..."]
#             }},
#             "inventory_forecast": {{
#                 "akan_habis": [
#                     {{"produk": "...", "estimasi_hari": 5}},
#                     {{"produk": "...", "estimasi_hari": 12}}
#                 ],
#                 "aman": ["...", "..."]
#             }},
#             "profit_forecast": {{
#                 "prediksi_profit_30_hari": "...",
#                 "status_margin": "naik/turun/stabil",
#                 "alasan_margin": "..."
#             }}
#         }}
#         """

#         client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
#         print(os.getenv("GOOGLE_API_KEY"))
#         response = client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=prompt
#         )

#         ai_result = response.text

#     except Exception as e:
#         print("Error koneksi:", e)
#         return {
#             "sales_forecast": {
#                 "prediksi_7_hari": "Tidak tersedia",
#                 "prediksi_30_hari": "Tidak tersedia",
#                 "tren": "Tidak tersedia",
#                 "alasan": "Koneksi API gagal"
#             },
#             "product_demand": {
#                 "produk_tertinggi": [],
#                 "produk_menurun": []
#             },
#             "inventory_forecast": {
#                 "akan_habis": [],
#                 "aman": []
#             },
#             "profit_forecast": {
#                 "prediksi_profit_30_hari": "Tidak tersedia",
#                 "status_margin": "Tidak tersedia",
#                 "alasan_margin": "Koneksi API gagal"
#             }
#         }

#     return ai_result
