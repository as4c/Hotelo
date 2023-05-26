from decimal import Decimal
from django.shortcuts import render , redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login,logout
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .models import (Amenities, Hotel, HotelBooking,Room_Type,Room)
from django.db.models import Q
from django.conf import settings
import stripe
from .forms import HotelBookingForm
from django.contrib.auth.decorators import login_required
from payment.models import BookingDetail
from django.db import models
from django.utils.dateparse import parse_date
from django.db.models import F
from datetime import datetime


stripe.api_key = settings.STRIPE_SECRET_KEY

def check_booking(start_date ,end_date ,uid ,rooms, room_count):
    if(len(HotelBooking.objects.all())<1):
        return True
    check_in_date = (start_date)
    check_out_date = (end_date)
    qs = HotelBooking.objects.filter(   
        start_date__lte=check_in_date,
        end_date__gte=check_out_date,
        hotel__uid = uid
        )
    
    # Calculate the total number of rooms already booked during the date range
    total_booked_rooms = qs.aggregate(models.Sum('no_of_room'))['no_of_room__sum'] or 0
    # Check if the hotel has enough available rooms
    return total_booked_rooms + int(rooms) <= room_count

## New Code Start
def home_page(request):
    return render(request , 'landing_page.html' )

def search_results(request):
    query = request.GET.get('query')
    amenities = Amenities.objects.all()
    if query:
        hotels = Hotel.objects.filter(
            Q(hotel_name__icontains=query) |
            Q(hotel_description__icontains=query)|
            Q(continent__icontains=query) |
            Q(country__name__icontains=query) |
            Q(region__name__icontains=query) |
            Q(city__name__icontains=query) |
            Q(landmark__icontains=query) 
        ).distinct()

        context = {
            'hotels': hotels,
            'query': query,
            'amenities':amenities
        }
        return render(request,'search_results.html',context)

@login_required
def details(request,uid):
    hotels=Hotel.objects.get(uid=uid)
    room_type = Room_Type.objects.filter(room__hotel=hotels).distinct()
    room=Room.objects.filter(hotel=hotels)
    form = HotelBookingForm()
    context={
        'hotels':hotels,
        'room_type':room_type,
        'room':room,
        'form':form,
    }
    return render(request,'details.html',context)


def room_availability(request):
    if request.method=='POST':
        uid=request.POST.get('uid')
        if uid is None:
            return JsonResponse({"error": "No hotel_id provided"})
        checkin = request.POST.get('check_in')
        checkout = request.POST.get('check_out')
        rooms = int(request.POST.get('room_count'))
        room_type=request.POST.get('room_type')

        try:
            hotel = Hotel.objects.get(uid=uid)
        except Hotel.DoesNotExist:
            return JsonResponse({"error": "Hotel not found"})
        # Check if the hotel has enough available rooms for the given date range and room count
        print("checkin: ",checkin)
        check_in = datetime.strptime(checkin, '%m/%d/%Y %I:%M %p')
        check_in_date = check_in.strftime('%Y-%m-%d')
        check_out = datetime.strptime(checkout, '%m/%d/%Y %I:%M %p')
        check_out_date = check_out.strftime('%Y-%m-%d')
        available = check_booking(check_in_date, check_out_date, uid, rooms, hotel.total_room)
        if not available:
            messages.warning(request, 'Hotel is already booked in these dates !!! Please Wait for some time or Try another dates !')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        messages.success(request,"Congrats,Hotel is available in these dates! Book Now")
        return JsonResponse({"available": available,"message":"Congrats,Room is available! Book Now"})
    return JsonResponse({"error": "Invalid request method"})
@login_required
def book_hotel(request):
    if request.method == 'POST':
        uid=request.POST.get('uid')
        hotel =Hotel.objects.get(uid=uid)
        form = HotelBookingForm(request.POST)
        if form.is_valid():
            # Save the booking data to the database
            booking = form.save(commit=False)
            booking.hotel=hotel
            booking.user = request.user # Assuming you have a User model and want to associate the booking with the current user
            booking.save()
            # Redirect the user to the booking detail page
            return redirect('booking_detail', pk=booking.pk)
    else:
        # If the request is not a POST request, create a new empty form
        form = HotelBookingForm()
    # Render the hotel detail template with the booking form included in the modal
    return render(request, 'hotel_booking.html', {'form': form,'pk':booking.pk})
 
def booking(request,uid):
    try:
        hotel = Hotel.objects.get(uid=uid)
        print("hotel: ",hotel)
    except Hotel.DoesNotExist:
        return JsonResponse({"error": "Hotel not found"})
    rooms = Room_Type.objects.filter(room__hotel=hotel).distinct()
    
    if request.method == 'POST':
        # get form data
    
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        room_type_name = request.POST.get('room_type')
        booking_type = request.POST.get('booking_type')
        no_of_room = int(request.POST.get('no_of_room'))
        no_of_people = request.POST.get('no_of_people')
        customer_desc = request.POST.get('customer_desc')

        check_in_date = parse_date(start_date)
        check_out_date = parse_date(end_date)
        

        # Calculate the number of nights between the check-in and check-out dates
        night_count = (check_out_date - check_in_date).days
        
        # Get the selected room object
        room = Room.objects.filter(hotel=hotel, rooms_type__type=room_type_name).first()
        room_type = Room_Type.objects.get(type=room_type_name)
        # Check if the room is available for the selected date range and room count
        available_count = room.room_count - room.booked_room
        if available_count < no_of_room:
            messages.error(request, f'Sorry, there are not enough available {room_type} rooms for the selected date range and room count.')
            return redirect('home:booking' ,hotel.uid)
        amount=room.price * night_count * no_of_room
        if booking_type == 'Pre Paid':
            amount = amount * Decimal('0.9')
        # create hotel booking instance
        hotel_booking = HotelBooking(
            hotel=hotel,
            user=request.user,
            start_date=start_date,
            end_date=end_date,
            room_type=room_type,
            amount=amount,
            booking_type=booking_type,
            no_of_room=no_of_room,
            no_of_people=no_of_people,
            customer_desc=customer_desc
        )
        # save hotel booking instance
        hotel_booking.save()
        print("Booking Data Saved")
        # redirect to booking detail page
        return redirect('home:booking_detail', uid=hotel_booking.uid)
    return render(request, 'booking_form.html', {'hotel': hotel, 'room_type': rooms})


@login_required
def bookingdetail(request, uid):
    booking = get_object_or_404(HotelBooking, uid=uid, user=request.user)
    end_datetime = datetime.combine(booking.end_date, datetime.min.time())
    start_datetime = datetime.combine(booking.start_date, datetime.min.time())
    total_days = (end_datetime - start_datetime).days 
    price = booking.amount
    rooms=booking.no_of_room
    obj=BookingDetail.objects.create(
        hotel=booking.hotel.hotel_name,
        user=request.user,
        start_date=booking.start_date,
        end_date=booking.end_date,
        total_days=total_days,
        total_room=rooms,
        total_amount=price,
        alloted_rooms=booking.room_number
        )
    return render(request, 'booking_detail.html', {'booking': booking,'uid':obj.uid})       


def AboutUs(request):
    return render(request,'about_us.html')

def ContactUs(request):
    return render(request,'contact_us.html')

''' New Codes End '''

def home(request):
    amenities_objs = Amenities.objects.all()
    hotels_objs = Hotel.objects.all()

    sort_by = request.GET.get('sort_by')
    search = request.GET.get('search')
    amenities = request.GET.getlist('amenities')
    if sort_by:
        if sort_by == 'ASC':
            hotels_objs = hotels_objs.order_by('hotel_price')
        elif sort_by == 'DSC':
            hotels_objs = hotels_objs.order_by('-hotel_price')

    if search:
        hotels_objs = hotels_objs.filter(
            Q(hotel_name__icontains = search) |
            Q(description__icontains = search) )


    if len(amenities):
        hotels_objs = hotels_objs.filter(amenities__amenity_name__in = amenities).distinct()

    context = {
        'amenities_objs' : amenities_objs , 
        'hotels_objs' : hotels_objs , 
        'sort_by' : sort_by ,
        'search' : search , 
        'amenities' : amenities
    }

    # return render(request , 'home.html' ,context)

