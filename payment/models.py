from django.db import models
from home.models import BaseModel,Hotel,HotelBooking
from django.contrib.auth.models import User
from django.conf import settings

class BookingDetail(BaseModel):
    hotel = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    start_date=models.DateField()
    end_date=models.DateField()
    total_days=models.IntegerField()
    total_room=models.IntegerField()
    total_amount=models.DecimalField(default=1.00,max_digits=10,decimal_places=2)
    alloted_rooms = models.CharField(max_length=10,blank=True,null=True)


class HotelBookingHistory(BaseModel):

    PENDING = "P"
    BOOKED = "B"
    FAILED = "F"
    REFUND = "R"

    STATUS_CHOICES = (
        (PENDING, ("pending")),
        (BOOKED, ("booked")),
        (FAILED, ("failed")),
        (REFUND,("refunded"))
    )

    booking_data= models.ForeignKey(BookingDetail , related_name="booking_detail" , on_delete=models.PROTECT)
    email = models.EmailField()
    amount=models.DecimalField(default=1.00,max_digits=10,decimal_places=2)
    booking_status = models.CharField(max_length=2,choices=STATUS_CHOICES,default='pending')
    payment_intent_id=models.CharField(max_length=255,null=True,blank=True)
    transaction_id=models.CharField(max_length=255,null=True,blank=True)
    invoice_id = models.CharField(max_length=50, blank=True, null=True)
    invoice_url = models.URLField(blank=True,null=True)
    def __str__(self):
        return f"{self.booking_data.hotel} booked by {self.booking_data.user}"
