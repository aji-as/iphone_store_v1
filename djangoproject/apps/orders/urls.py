from django.urls import path
from .views import index, cekpesanan ,order_sukses


app_name = 'orders'

urlpatterns =[
    path('<int:id_product>/', index, name='index'),
    path('cekpesanan/', cekpesanan, name='cekpesanan'),
]