from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Amenities)
admin.site.register(Hotel)
admin.site.register(HotelImages)
admin.site.register(HotelBooking)
admin.site.register(Room)
admin.site.register(Room_Type)
# admin.site.register(Address)
# admin.site.register(Hotel_Address)