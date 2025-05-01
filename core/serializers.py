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
        fields = ['trip', 'seat_number']  # Passenger will come from logged-in user

    def validate(self, data):
        trip = data.get('trip')
        seat_number = data.get('seat_number')

        # Check if seat already booked
        if Ticket.objects.filter(trip=trip, seat_number=seat_number).exists():
            raise serializers.ValidationError("Seat already booked for this trip.")
        return data

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'trip', 'seat_number']

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'route', 'departure_time', 'arrival_time']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'sent_time']

