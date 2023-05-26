
from django import forms
from .models import HotelBooking

class HotelBookingForm(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = ['start_date', 'end_date', 'room_type', 'booking_type', 'no_of_room','no_of_people','customer_desc']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

