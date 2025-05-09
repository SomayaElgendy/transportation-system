from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  

#User with different role choices
class Profile(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('STAFF', 'Staff'),
        ('PASSENGER', 'Passenger'),
        ('DRIVER', 'Driver'),
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
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'DRIVER'}
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    STATUS_CHOICES = [
        ('on_time', 'On Time'),
        ('delayed', 'Delayed'),
        ('cancelled', 'Cancelled'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='on_time')

    def __str__(self):
        return f"{self.route} - {self.departure_time.strftime('%Y-%m-%d %H:%M')}"


class Ticket(models.Model):
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE)
    passenger = models.ForeignKey('Profile', on_delete=models.CASCADE)
    seat_number = models.PositiveIntegerField()
    booking_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('trip', 'seat_number') 

    def __str__(self):
        return f"Seat {self.seat_number} - {self.passenger.username}"
    


class Payment(models.Model):
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_time = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50)  # Example: Credit Card, PayPal

    def __str__(self):
        return f"{self.amount} paid on {self.payment_time}"


class Notification(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    sent_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification at {self.sent_time} for {self.user.username}"
