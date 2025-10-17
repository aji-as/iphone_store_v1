from django.urls import path
from .views import index, cekpesanan


app_name = 'orders'

urlpatterns =[
    path('<int:id_product>/', index, name='index'),
    path('cekpesanan/', cekpesanan, name='cekpesanan'),
]