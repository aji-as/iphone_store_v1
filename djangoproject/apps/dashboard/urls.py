from django.urls import path
from . views import index, datasales, productlist , addproduct , deleteproduct,editproduct,sendorder 
app_name = 'dashboard'
urlpatterns =[ 
    path('sendorder/<str:order_id>', sendorder, name='sendorder'),
    path('editproduct/<int:id_product>', editproduct, name='editproduct'),
    path('deleteproduct/<int:id_product>', deleteproduct , name='deleteproduct'),
    path('addproduct', addproduct , name='addproduct'),
    path('datasales', datasales , name='datasales'),
    path('productlist', productlist , name='productlist'),
    path('', index , name='index')
]




