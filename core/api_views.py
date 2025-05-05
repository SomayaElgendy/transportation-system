from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from core.models import Trip, Ticket, Notification
from core.serializers import TripSerializer, BookingSerializer, TicketSerializer, NotificationSerializer
from rest_framework.permissions import IsAuthenticated

#API to let a logged-in user book a ticket
@api_view(['POST'])
@permission_classes([IsAuthenticated])  #user must be logged in
def book_ticket_api(request):
    serializer = BookingSerializer(data=request.data) #validates the input
    # if the input is valdi, savee the ticket and send it to passenger
    if serializer.is_valid():
        ticket = serializer.save(passenger=request.user)
        return Response({"message": "Ticket booked successfully!"})
    # if not, return response 400 code (invalid data) 
    return Response(serializer.errors, status=400)

#API shows the logged-in user their booked tickets
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_tickets(request):
    tickets = Ticket.objects.filter(passenger=request.user) #show only the user's tickets
    serializer = TicketSerializer(tickets, many=True) # change (serialize) tickets format/type
    return Response(serializer.data)

#API that returns a list of all trips to anyone
@api_view(['GET'])
def trip_list(request):
    trips = Trip.objects.all()
    serializer = TripSerializer(trips, many=True)
    return Response(serializer.data)

#API shows notifications for the logged-in user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_notifications_api(request):
    #show user's notification ordered by the time sent
    notifications = Notification.objects.filter(user=request.user).order_by('-sent_time')
    #notifications in list by serializer
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


