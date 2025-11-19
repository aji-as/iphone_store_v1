from django.urls import path
from .views import index , detailproduct , daftarproduct

app_name = 'items'
urlpatterns =[
    path('detailproduct/<int:id_product>', detailproduct  , name='detailproduct' ),
    path('listproduct', daftarproduct  , name='listproduct' ),
    path('', index , name='index' )
]
