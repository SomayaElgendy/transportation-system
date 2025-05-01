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
from .decorators import staff_required 
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone


# Create your views here.
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




def trip_list(request):
    form = TripSearchForm(request.GET or None)
    trips = Trip.objects.all()

    if form.is_valid():
        start_town = form.cleaned_data['start_town']  # This should be a Town instance
        end_town = form.cleaned_data['end_town']     # This should be a Town instance
        departure_date = form.cleaned_data['departure_date']

        # Filter trips based on search fields
        trips = trips.filter(
            route__start_town=start_town,  # Changed from route__start
            route__end_town=end_town,       # Changed from route__end
        )

        if departure_date:
            trips = trips.filter(departure_time__date=departure_date)

        trips = trips.order_by('departure_time')

    return render(request, 'core/trip_list.html', {
        'trips': trips,
        'form': form
    })


@login_required
def book_ticket(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    taken_seats = Ticket.objects.filter(trip=trip).values_list('seat_number', flat=True)
    all_seats = range(1, trip.bus.capacity + 1)
    available_seats = [seat for seat in all_seats if seat not in taken_seats]

    if request.method == 'POST':
        form = BookingForm(request.POST, available_seats=available_seats)
        if form.is_valid():
            seat_number = form.cleaned_data['seat_number']  # Now already an int
            payment_method = form.cleaned_data['payment_method']

            if seat_number not in available_seats:
                return render(request, 'core/book_ticket.html', {
                    'trip': trip,
                    'form': form,
                    'available_seats': available_seats,
                    'error': 'Seat already booked. Please choose another.'
                })

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

            return render(request, 'core/booking_success.html', {
                'trip': trip,
                'seat_number': seat_number,
                'payment_method': payment_method
            })

    else:
        form = BookingForm(available_seats=available_seats)

    return render(request, 'core/book_ticket.html', {
        'trip': trip,
        'form': form,
        'available_seats': available_seats
    })


def booking_success(request):
    return render(request, 'core/booking_success.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # 🔥 Role-based redirection
            if user.role == 'ADMIN':
                return redirect('admin_dashboard')
            elif user.role == 'STAFF':
                return redirect('staff_dashboard')
            elif user.role == 'PASSENGER':
                return redirect('trip_list')  # Passengers see trips
            elif user.role == 'DRIVER':
                return redirect('driver_dashboard')

            # default fallback
            return redirect('dashboard')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid username or password'})
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


@login_required
@admin_required
def admin_financial_report(request):
    payments = Payment.objects.all()
    total_revenue = sum(payment.amount for payment in payments)

    return render(request, 'core/admin_financial_report.html', {
        'payments': payments,
        'total_revenue': total_revenue
    })

@login_required
@driver_required
def view_assigned_trips(request):
    trips = Trip.objects.filter(driver=request.user)
    return render(request, 'core/driver_assigned_trips.html', {'trips': trips})

@login_required
@driver_required
def report_trip_status(request):
    trips = Trip.objects.filter(driver=request.user)

    if request.method == 'POST':
        trip_id = request.POST.get('trip_id')
        status = request.POST.get('status')
        trip = Trip.objects.get(id=trip_id, driver=request.user)
        trip.status = status
        trip.save()
        messages.success(request, 'Trip status updated successfully!') 
        return redirect('driver_dashboard')

    return render(request, 'core/report_trip_status.html', {'trips': trips})

def signup_passenger(request):
    if request.method == 'POST':
        form = PassengerSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'PASSENGER'
            user.save()
            return redirect('login')  # or auto-login
    else:
        form = PassengerSignupForm()
    
    return render(request, 'core/signup.html', {'form': form})





