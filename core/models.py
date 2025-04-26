from django.db import models
from django.contrib.auth.models import AbstractUser

#User with different role choices
class Profile(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('passenger', 'Passenger'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Town(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Route(models.Model):
    start_town = models.CharField(max_length=100)  # Later: ForeignKey to Town
    end_town = models.CharField(max_length=100)    # Later: ForeignKey to Town
    duration = models.DurationField()

    def __str__(self):
        return f"{self.start_town} ➔ {self.end_town}"


class Bus(models.Model):
    bus_number = models.CharField(max_length=20)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.bus_number


class Trip(models.Model):
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    route_name = models.CharField(max_length=100)  # Later: ForeignKey to Route
    bus_number = models.CharField(max_length=20)   # Later: ForeignKey to Bus

    def __str__(self):
        return f"Trip {self.route_name} at {self.departure_time}"


class Ticket(models.Model):
    seat_number = models.PositiveIntegerField()
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Seat {self.seat_number}"


class Payment(models.Model):
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_time = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50)  # Example: Credit Card, PayPal

    def __str__(self):
        return f"{self.amount} paid on {self.payment_time}"


class Notification(models.Model):
    message = models.TextField()
    sent_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification at {self.sent_time}"
