from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Trip, Ticket, Profile, Notification, Payment
from .forms import TicketForm, TripSearchForm, PassengerSignupForm, BookingForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import admin_required, staff_required, driver_required
from django.db import transaction
from django.db import IntegrityError
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone


# Create your views here.

#redirecting according to role
def home(request):
    if request.user.is_authenticated:
        if request.user.role == 'ADMIN':
            return redirect('admin_dashboard')
        elif request.user.role == 'STAFF':
            return redirect('staff_dashboard')
        elif request.user.role == 'DRIVER':
            return redirect('driver_dashboard')
        elif request.user.role == 'PASSENGER':
            return redirect('trip_list')
    
    return render(request, 'core/home.html')

#Show trips with option to filter by towns and date
def trip_list(request):
    #use whatever filters or pass none
    form = TripSearchForm(request.GET or None)
    trips = Trip.objects.all()
    #checks if form is valid
    if form.is_valid():
        start_town = form.cleaned_data['start_town']  
        end_town = form.cleaned_data['end_town']     
        departure_date = form.cleaned_data['departure_date']

        #Filter trips based on search fields
        trips = trips.filter(
            route__start_town=start_town, 
            route__end_town=end_town,    
        )

        if departure_date:
            trips = trips.filter(departure_time__date=departure_date)
        trips = trips.order_by('departure_time')
    #then gets the trip list and applys the form filters if used
    return render(request, 'core/trip_list.html', {
        'trips': trips,
        'form': form
    })

#Book ticket, validate seat, create ticket & payment, notify user
@login_required
def book_ticket(request, trip_id):
    #try to find the trip, if not found, show a 404 error.
    trip = get_object_or_404(Trip, id=trip_id)
    #taken seats are the seats in the tickets (booked)
    taken_seats = Ticket.objects.filter(trip=trip).values_list('seat_number', flat=True)
    #all seats are from the range of the bus capacity
    all_seats = range(1, trip.bus.capacity + 1)
    # available seats are the ones not in taken_seats using comprehensive list with loop
    available_seats = [seat for seat in all_seats if seat not in taken_seats]

    #now we use POST to book 
    if request.method == 'POST':
        #loads the booking form with the available seats
        form = BookingForm(request.POST, available_seats=available_seats)

        if form.is_valid():
            # get seat number and payemnt method
            seat_number = form.cleaned_data['seat_number']  
            payment_method = form.cleaned_data['payment_method']

            #just double check if the seat in not available show message
            if seat_number not in available_seats:
                return render(request, 'core/book_ticket.html', {
                    'trip': trip,
                    'form': form,
                    'available_seats': available_seats,
                    'error': 'Seat already booked. Please choose another.'
                })
            #Now using concurrency transaction.atomic to update seat availability safely 
            #create the ticket, payment and send notification
            with transaction.atomic():
                # Create Ticket
                ticket = Ticket.objects.create(
                    trip=trip,
                    seat_number=seat_number,
                    passenger=request.user
                )

                # Create Payment
                Payment.objects.create(
                    amount=50.00,
                    method=payment_method,
                    ticket=ticket,
                    payment_time=timezone.now()
                )

                Notification.objects.create(
                    user=request.user,
                    sent_time=timezone.now(),
                    message=f"You successfully booked Seat {seat_number} on Trip {trip.id}.")
                
                send_mail(
                    subject='Booking Confirmation',
                    message=f"You successfully booked Seat {seat_number} on Trip {trip.id}.",
                    from_email=None,
                    recipient_list=[request.user.email],
                    fail_silently=False)

            #redirect to booking successful page with booking detials
            return render(request, 'core/booking_success.html', {
                'trip': trip,
                'seat_number': seat_number,
                'payment_method': payment_method
            })
    #if the user didnt submit the booking form, just keep showing the form with available seats
    else:
        form = BookingForm(available_seats=available_seats)
    #Show the booking form page
    return render(request, 'core/book_ticket.html', {
        'trip': trip,
        'form': form,
        'available_seats': available_seats
    })

#booking successful page 
def booking_success(request):
    return render(request, 'core/booking_success.html')

#Logging function
def login_view(request):
    #user will enter credintials
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #authenticate
        user = authenticate(request, username=username, password=password)
        #if authenticated, redirect based on acc type
        if user is not None:
            login(request, user)

            #Role-based redirection
            if user.role == 'ADMIN':
                return redirect('admin_dashboard')
            elif user.role == 'STAFF':
                return redirect('staff_dashboard')
            elif user.role == 'PASSENGER':
                return redirect('trip_list')  # Passengers see trips
            elif user.role == 'DRIVER':
                return redirect('driver_dashboard')

            #default just in case
            return redirect('dashboard')
        #if not, go back to login page and show message
        else:
            return render(request, 'core/login.html', {'error': 'Invalid username or password'})
    #stay on login page if user didnt login
    return render(request, 'core/login.html')


@login_required
@admin_required
def admin_dashboard(request):
    return render(request, 'core/admin_dashboard.html')

@login_required
@staff_required
def staff_dashboard(request):
    return render(request, 'core/staff_dashboard.html')

@login_required
@driver_required
def driver_dashboard(request):
    return render(request, 'core/driver_dashboard.html')

@login_required
def dashboard(request):
    profile = request.user
    return render(request, 'core/dashboard.html', {'profile': profile})

def logout_view(request):
    logout(request)
    return redirect('login')

#staff pages
@login_required
@staff_required
def staff_view_trips(request):
    trips = Trip.objects.all()
    return render(request, 'core/staff_trips.html', {'trips': trips})

@login_required
@staff_required
def staff_view_tickets(request):
    tickets = Ticket.objects.all()
    return render(request, 'core/staff_tickets.html', {'tickets': tickets})

@login_required
@staff_required
def staff_view_payments(request):
    payments = Payment.objects.all()
    return render(request, 'core/staff_payments.html', {'payments': payments})

#admin revenue calculation
@login_required
@admin_required
def admin_financial_report(request):
    payments = Payment.objects.all()
    total_revenue = sum(payment.amount for payment in payments)

    return render(request, 'core/admin_financial_report.html', {
        'payments': payments,
        'total_revenue': total_revenue
    })

#driver can only view his trips
@login_required
@driver_required
def view_assigned_trips(request):
    trips = Trip.objects.filter(driver=request.user)
    return render(request, 'core/driver_assigned_trips.html', {'trips': trips})

#driver can report the trip status
@login_required
@driver_required
def report_trip_status(request):
    #driver's trips
    trips = Trip.objects.filter(driver=request.user)
    #driver updating the trip status and then saved and notified
    if request.method == 'POST':
        trip_id = request.POST.get('trip_id')
        status = request.POST.get('status')
        trip = Trip.objects.get(id=trip_id, driver=request.user)
        trip.status = status
        trip.save()
        messages.success(request, 'Trip status updated successfully!') 
        #redirect to dashboard
        return redirect('driver_dashboard')
    #stay on report trip status page if driver did nothing
    return render(request, 'core/report_trip_status.html', {'trips': trips})

#signing in as passenger
def signup_passenger(request):
    if request.method == 'POST':
        #the form is filled and checked, then saved 
        form = PassengerSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'PASSENGER'
            user.save()
            return redirect('login') 
    #or just show form
    else:
        form = PassengerSignupForm()
    # and stayy on page
    return render(request, 'core/signup.html', {'form': form})





