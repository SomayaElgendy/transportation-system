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

# Unregister old Trip registration if it exists
try:
    admin.site.unregister(Trip)
except admin.sites.NotRegistered:
    pass

# Register Trip with custom TripAdmin
class TripAdmin(admin.ModelAdmin):
    list_display = ('route', 'bus', 'driver', 'departure_time', 'arrival_time')
    list_filter = ('route', 'departure_time', 'driver')

admin.site.register(Trip, TripAdmin)


