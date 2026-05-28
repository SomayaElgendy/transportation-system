from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Trip, Bus, Route, Town, Ticket, Payment, Notification, LostItem

@admin.register(Profile)
class ProfileAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )

    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')


admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(Town)
admin.site.register(Ticket)
admin.site.register(Payment)
admin.site.register(Notification)


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('route', 'bus', 'driver', 'departure_time', 'arrival_time')
    list_filter = ('route', 'departure_time', 'driver')

@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'passenger', 'trip', 'status', 'reported_time')
    list_filter = ('status', 'reported_time')
    search_fields = ('item_name', 'description', 'passenger__username')