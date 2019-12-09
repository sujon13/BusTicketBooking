from django.shortcuts import render
from .models import Bus, Trip


def index(request):
    number_of_buses = Trip.objects.count()
    bus_list = Bus.objects.all()
    context = {'number_of_buses': number_of_buses, 'busList': bus_list}
    return render(request, 'busTicketBooking/index.html', context)

