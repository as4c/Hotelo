from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
import uuid
from smart_selects.db_fields import ChainedForeignKey
from cities_light.models import City, Country, Region
from django.http import JsonResponse,HttpResponse
from django.conf import settings

class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False , primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True




class Amenities(BaseModel):
    amenity_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.amenity_name




class Hotel(BaseModel):
    CONTINENT_CHOICES = [
        ('AF', 'Africa'),
        ('AN', 'Antarctica'),
        ('AS', 'Asia'),
        ('EU', 'Europe'),
        ('NA', 'North America'),
        ('OC', 'Oceania'),
        ('SA', 'South America'),
    ]

    hotel_name= models.CharField(max_length=100)
    hotel_email=models.EmailField(default='your@mail.com')
    hotel_phone=models.CharField(max_length=15,default='9876543210')
    hotel_description = models.TextField()
    hotel_amenities = models.ManyToManyField(Amenities)
    # hotel_rooms=models.ManyToManyField('Room',related_name='hotel_rooms')
    total_room = models.IntegerField(default=0)
    total_booked_room=models.IntegerField(default=0)
    total_staffs=models.IntegerField(default=10)
    is_avail=models.BooleanField(default=True)
    #Address
    continent = models.CharField(max_length=2, choices=CONTINENT_CHOICES)
    country = ChainedForeignKey(Country,chained_field="continent",chained_model_field="continent",show_all=False, on_delete=models.CASCADE)
    region= ChainedForeignKey(Region,chained_field="country",chained_model_field="country_id",show_all=False,on_delete=models.CASCADE)
    city = ChainedForeignKey(City, chained_field="region",chained_model_field="region_id",show_all=False,on_delete=models.CASCADE)
    street=models.CharField(max_length=100)
    landmark=models.CharField(max_length=100,default='GMT')
    zip_code=models.CharField(max_length=20,default='000000')


    def __str__(self) -> str:
        return self.hotel_name   

    def is_hotel_available(self):
        return True if self.total_room > self.total_booked_room else False
    
    def total_client(self):
        return 1000 + self.total_booked_room

class Room_Type(BaseModel):
    OTHERS='O'
    SINGLE='SL'
    DOUBLE='D'
    DELUX='DD'
    SUITE='ST'
    DOORMATORY='DT'
    ROOM_CHOICES=[
        ('SINGLE',('Single')),
        ('DOUBLE',('Double')),
       ('DELUX',('Delux')),
       ('SUITE',('Suite')),
       ('DOORMATORY',('Doormatory')),
       ('OTHERS',('Others'))
    ]
   
    type=models.CharField(max_length=10,choices=ROOM_CHOICES)
    room_description=models.TextField()
    room_image=models.ImageField(upload_to="room_type_images")
    facilities=models.ManyToManyField(Amenities)
    max_occupancy=models.IntegerField(default=1)
    

    def __str__(self) -> str:
        return self.type


 
class Room(BaseModel):   
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name='related_hotel_name',default="")
    rooms_type=models.ForeignKey(Room_Type, on_delete=models.CASCADE)
    room_number=models.IntegerField(default=1)
    floor=models.CharField(max_length=10)
    price=models.DecimalField(decimal_places=2,default=999.00,max_digits=10)
    room_count=models.IntegerField(default=10)
    room_image=models.ImageField(upload_to="room_image" ,default='loading.gif')
    booked_room=models.IntegerField(default=0)
    is_available=models.BooleanField(default=True)

    def available(self):
        totalroom=self.hotel.total_room
        if self.booked_room >= self.totalroom:
            self.is_available=False
        return self.is_available

        

    def __str__(self) -> str:
        return f'Rooms of {self.hotel.hotel_name}'
    
    def save(self, *args, **kwargs):
        self.room_number +=1
        
      
        super().save(*args, **kwargs)
 
 

class HotelImages(BaseModel):
    hotel= models.ForeignKey(Hotel ,related_name="images", on_delete=models.CASCADE)
    images = models.ImageField(upload_to="hotels")


class HotelBooking(BaseModel):
    hotel= models.ForeignKey(Hotel, related_name="hotel_booking_detail" , on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_booking_detail" , on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    room_type=models.ForeignKey(Room_Type,on_delete=models.PROTECT,related_name='booked_room_type',default=0)
    amount=models.DecimalField(default=0.00,decimal_places=2,max_digits=10)
    booking_type = models.CharField(max_length=100, choices=(('Pre Paid', 'Pre Paid'), ('Post Paid', 'Post Paid')))
    no_of_room = models.IntegerField(default=1)
    room_number=models.IntegerField(blank=True, null=True)
    no_of_people=models.IntegerField()
    customer_desc=models.CharField(max_length=100)


    def __str__(self):
        return f"{self.user}'s booked a room at {self.hotel.hotel_name}"
    
    def save(self, *args, **kwargs):
        # Get all the bookings for this hotel during the same time period
     
        conflicting_bookings = HotelBooking.objects.filter(
            hotel=self.hotel,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date,
        ).exclude(uid=self.uid)
       
        
        # Find the next available room number for this booking
        last_booking = HotelBooking.objects.filter(hotel=self.hotel).order_by('-room_number').first()
        next_room_number = (last_booking.room_number + 1) if last_booking else 1
        
        # Assign the next available room number to this booking
        self.room_number = next_room_number
        self.hotel.total_room -=self.no_of_room
        # Call the superclass's save method to save the booking to the database
        super().save(*args, **kwargs)
    
