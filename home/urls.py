from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name  = 'home'
urlpatterns = [
    path('',home_page,name='home'),
    path('search/',search_results,name='search'),
    path('details/<str:uid>/', details , name='detail'),
    path('check_avail/' , room_availability,name="check_room_avail"),
    path('book-hotel/<str:uid>',booking,name='booking'),
    path('booking-detail/<str:uid>/',bookingdetail,name='booking_detail'),
    path('about-us/',AboutUs,name='about_us'),
    path('contact-us/',ContactUs,name='contact_us'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()