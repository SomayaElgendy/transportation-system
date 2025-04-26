from django.shortcuts import render
from django.http import HttpResponse
from .models import Trip

# Create your views here.
def home(request):
    return HttpResponse("<h1>Welcome to the Transportation System</h1>")


def trip_list(request):
    trips = Trip.objects.all()
    return render(request, 'core/trip_list.html', {'trips': trips})
