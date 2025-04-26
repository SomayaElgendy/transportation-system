from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Trip, Ticket, Profile
from .forms import TicketForm

# Create your views here.
def home(request):
    return HttpResponse("<h1>Welcome to the Transportation System</h1>")


def trip_list(request):
    trips = Trip.objects.all()
    return render(request, 'core/trip_list.html', {'trips': trips})

def book_ticket(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)

    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.trip = trip
            # Assuming the user is logged in and has Profile
            ticket.passenger = request.user.profile
            ticket.save()
            return HttpResponse("Booking successful!")
    else:
        form = TicketForm()

    return render(request, 'core/book_ticket.html', {'form': form, 'trip': trip})
