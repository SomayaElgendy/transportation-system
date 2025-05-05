from django.contrib import admin
from .models import Profile, Trip, Bus, Route, Town, Ticket, Payment, Notification

# Register your models here.

admin.site.register(Profile)
admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(Town)
admin.site.register(Ticket)
admin.site.register(Payment)
admin.site.register(Notification)

#the coming lines are for adding driver field in Trip, so I unregistered trip and added it again bcs I forgot to add it at the beginning
try:
    admin.site.unregister(Trip)
except admin.sites.NotRegistered:
    pass

class TripAdmin(admin.ModelAdmin):
    list_display = ('route', 'bus', 'driver', 'departure_time', 'arrival_time')
    list_filter = ('route', 'departure_time', 'driver')

admin.site.register(Trip, TripAdmin)


