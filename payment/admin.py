from django.contrib import admin

from .models import BookingDetail,HotelBookingHistory

admin.site.register(BookingDetail)
admin.site.register(HotelBookingHistory)

