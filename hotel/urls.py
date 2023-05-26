
from django.contrib import admin
from django.urls import path,include

urlpatterns = [   
    path('' , include('home.urls')),
    path('payment/', include('payment.urls')), 
    path('auth/', include('auth_app.urls')),
    path('chaining/', include('smart_selects.urls')),
    path('admin/', admin.site.urls),

]
