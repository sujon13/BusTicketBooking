from django.contrib import admin

from .models import Bus, Trip, Seat, TripSeat, Passenger, Reservation


admin.site.register(Bus)
admin.site.register(Trip)
admin.site.register(Seat)
admin.site.register(TripSeat)
admin.site.register(Passenger)
admin.site.register(Reservation)