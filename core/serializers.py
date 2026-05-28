'''This file is used to define how our models are converted to JSON format 
and validated for API use. These serializers make sure we send and receive clean, 
structured data between the backend and the frontend or mobile apps.
'''
from rest_framework import serializers
from .models import Ticket, Notification, Trip

class TripSerializer(serializers.ModelSerializer):
    route = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = ['id', 'route', 'departure_time', 'arrival_time']

    def get_route(self, obj):
        return f"{obj.route.start_town} ➔ {obj.route.end_town}"
    

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['trip', 'seat_number']  
    #-----Security modification
    def validate(self, data):
        trip = data.get('trip')
        seat_number = data.get('seat_number')

        if seat_number < 1 or seat_number > trip.bus.capacity:
            raise serializers.ValidationError(
                f"Seat number must be between 1 and {trip.bus.capacity}."
            )
    #-----------------------
        if Ticket.objects.filter(trip=trip, seat_number=seat_number).exists():
            raise serializers.ValidationError("Seat already booked for this trip.")

        return data

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'trip', 'seat_number']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'sent_time']

