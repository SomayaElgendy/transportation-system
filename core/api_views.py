from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from core.models import Trip, Ticket, Notification
from core.serializers import TripSerializer, BookingSerializer, TicketSerializer, NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_ticket_api(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        ticket = serializer.save(passenger=request.user)
        return Response({"message": "Ticket booked successfully!"})
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_tickets(request):
    tickets = Ticket.objects.filter(passenger=request.user)
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def trip_list(request):
    trips = Trip.objects.all()
    serializer = TripSerializer(trips, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@login_required
def my_notifications_api(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-sent_time')
    data = [
        {
            "message": n.message,
            "sent_time": n.sent_time.strftime('%Y-%m-%d %H:%M:%S')
        }
        for n in notifications
    ]
    return Response(data)

