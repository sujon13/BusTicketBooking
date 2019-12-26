from django.contrib import admin

from .models import Bus, Trip, Seat


admin.site.register(Bus)
admin.site.register(Trip)
admin.site.register(Seat)
