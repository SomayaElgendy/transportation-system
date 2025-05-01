from django.test import TestCase
from .models import Ticket, Trip, Payment
from .forms import BookingForm
from django.urls import reverse
# Create your tests here.

class BookingFormTest(TestCase):
    def setUp(self):
        # Create necessary objects for testing (e.g., trip, ticket)
        self.trip = Trip.objects.create(...)
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
        self.trip = Trip.objects.create(...)
        self.client.login(username='user', password='password')

    def test_book_ticket_success(self):
        response = self.client.post(reverse('book_ticket', args=[self.trip.id]), data={
            'seat_number': 1,
            'payment_method': 'cash',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Booking Successful!")
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Payment.objects.count(), 1)

class DashboardViewTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user('admin', 'admin@example.com', 'password')
        self.staff = User.objects.create_user('staff', 'staff@example.com', 'password')
        self.driver = User.objects.create_user('driver', 'driver@example.com', 'password')

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
