
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', include('apps.items.urls', namespace='items')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    path('admin/', admin.site.urls),
   
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

