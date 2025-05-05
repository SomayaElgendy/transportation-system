from django import forms
from .models import Ticket, Town, Profile
from django.contrib.auth.forms import UserCreationForm

#this form is used for ticket creation (only asks for seat number)
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['seat_number']  #Only ask user for seat number


PAYMENT_CHOICES = [
    ('cash', 'Cash'),
    ('card', 'Credit/Debit Card'),
]
#Booking form for selecting a seat and payment method
class BookingForm(forms.Form):
    def __init__(self, *args, available_seats=None, **kwargs):
        super().__init__(*args, **kwargs)
        if available_seats:
            #Ensures seat numbers are available
            self.fields['seat_number'].choices = [(seat, f"Seat {seat}") for seat in available_seats]

    #seat numbers converted to int automatically
    seat_number = forms.TypedChoiceField( 
        label='Seat number',
        choices=[],  #filled in _init_
        coerce=int,  
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    #Payment method dropdown
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        label='Payment Method',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

#forms for the trip search filters
class TripSearchForm(forms.Form):
    start_town = forms.ModelChoiceField(
        queryset=Town.objects.all(),
        label="Start Town"
    )
    end_town = forms.ModelChoiceField(
        queryset=Town.objects.all(),
        label="End Town"
    )
    departure_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Departure Date"
    )

#form for signing up by django's sign up meta class
class PassengerSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password1', 'password2']

