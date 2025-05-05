from django.test import TestCase
from .models import Ticket, Trip, Payment, Route, Bus, Town
from .forms import BookingForm
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
# Create your tests here.

User = get_user_model()

class BookingFormTest(TestCase):
    def setUp(self):
        #Create objects for testing
        self.origin = Town.objects.create(name="Taif")
        self.destination = Town.objects.create(name="Yanbu")
        self.route = Route.objects.create(start_town=self.origin, end_town=self.destination, duration=timedelta(minutes=120))
        self.bus = Bus.objects.create(bus_number="ABC123", capacity=50)
        self.trip = Trip.objects.create(
        bus=self.bus,
        route=self.route,
        departure_time=datetime.now() + timedelta(days=1),
        arrival_time=datetime.now() + timedelta(days=1, hours=2)  )

        self.form_data = {
            'seat_number': 1,
            'payment_method': 'cash',
        }

    def test_valid_booking_form(self):
        form = BookingForm(data=self.form_data, available_seats=[1, 2, 3])
        self.assertTrue(form.is_valid())

    def test_invalid_seat_number(self):
        form = BookingForm(data=self.form_data, available_seats=[1, 2, 3])
        form.data['seat_number'] = 5
        self.assertFalse(form.is_valid())


class BookTicketViewTest(TestCase):
    def setUp(self):
        #Create user and login
        self.user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='password'
        )
        self.user.role = 'PASSENGER'
        self.user.save()

        self.client.login(username='user', password='password')

        self.origin = Town.objects.create(name="Jazan")
        self.destination = Town.objects.create(name="Aseer")

        self.route = Route.objects.create(
            start_town=self.origin,
            end_town=self.destination,
            duration=timedelta(minutes=90)
        )

        self.bus = Bus.objects.create(
            bus_number="XYZ987",
            capacity=40
        )

        self.trip = Trip.objects.create(
            bus=self.bus,
            route=self.route,
            departure_time=datetime.now() + timedelta(days=1),
            arrival_time=datetime.now() + timedelta(days=1, hours=2)
        )


    def test_book_ticket_success(self):
        response = self.client.post(reverse('book_ticket', args=[self.trip.id]), data={
            'seat_number': 1,
            'payment_method': 'cash', })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Booking Successful!")
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Payment.objects.count(), 1)


class DashboardViewTest(TestCase):
    #Create accounts
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', email='admin@example.com', password='password')
        self.admin.role = 'ADMIN'
        self.admin.save()

        self.staff = User.objects.create_user(username='staff', email='staff@example.com', password='password')
        self.staff.role = 'STAFF'
        self.staff.save()

        self.driver = User.objects.create_user(username='driver', email='driver@example.com', password='password')
        self.driver.role = 'DRIVER'
        self.driver.save()

    def test_admin_dashboard(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_staff_dashboard(self):
        self.client.login(username='staff', password='password')
        response = self.client.get(reverse('staff_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_driver_dashboard(self):
        self.client.login(username='driver', password='password')
        response = self.client.get(reverse('driver_dashboard'))
        self.assertEqual(response.status_code, 200)
