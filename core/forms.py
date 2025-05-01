from django import forms
from .models import Ticket, Town, Profile
from django.contrib.auth.forms import UserCreationForm


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['seat_number']  # Only ask user for seat number


PAYMENT_CHOICES = [
    ('cash', 'Cash'),
    ('card', 'Credit/Debit Card'),
]

class BookingForm(forms.Form):
    def __init__(self, *args, available_seats=None, **kwargs):
        super().__init__(*args, **kwargs)
        if available_seats:
            # Ensure seat numbers are stored as integers
            self.fields['seat_number'].choices = [(seat, f"Seat {seat}") for seat in available_seats]

    seat_number = forms.TypedChoiceField(  # Changed to TypedChoiceField
        label='Seat number',
        choices=[],  # Will be populated in __init__
        coerce=int,  # Convert to integer automatically
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        label='Payment Method',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

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

class PassengerSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password1', 'password2']

