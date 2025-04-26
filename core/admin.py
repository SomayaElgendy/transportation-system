from django.contrib import admin
from .models import Profile, Trip, Bus, Route, Town, Ticket, Payment, Notification

# Register your models here.

admin.site.register(Profile)
admin.site.register(Trip)
admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(Town)
admin.site.register(Ticket)
admin.site.register(Payment)
admin.site.register(Notification)

