from django.contrib import admin

from .models import Bus, Trip, Seat, TripSeat


admin.site.register(Bus)
admin.site.register(Trip)
admin.site.register(Seat)
admin.site.register(TripSeat)
