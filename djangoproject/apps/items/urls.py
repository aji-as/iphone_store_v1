from django.urls import path
from .views import index , detailproduct 

app_name = 'items'
urlpatterns =[
    path('detailproduct/<int:id_product>', detailproduct  , name='detailproduct' ),
    path('', index , name='index' )
]
