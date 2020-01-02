from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import json
from .models import Bus, Trip, Seat, TripSeat
from .forms import SearchBus
from datetime import datetime


def home(request):
    # create a form instance and populate it with data from the request:
    form = SearchBus(request.GET)
    if form.is_valid():
        start_station = form.cleaned_data['start_station']
        destination = form.cleaned_data['destination']
        date_of_journey = form.cleaned_data['date_of_journey']
        trip_list = get_trip_list(start_station, destination, date_of_journey)
        seat_info = get_seat_info(trip_list[0])
        context = {'number_of_buses': trip_list.count(), 'trip': trip_list[0],
                   'seat_info': json.dumps(seat_info)}
        return render(request, 'busTicketBooking/thanks.html', context)

    else:
        form = SearchBus()

    return render(request, 'busTicketBooking/home.html', {'form': form})


# helper function for home.html

def convert_string_to_date(date_of_journey):
    # string to date
    journey_date = datetime.strptime(date_of_journey, "%m/%d/%Y").date()
    # date to string(in format: %Y-%m-%d)
    journey_date = journey_date.strftime("%Y-%m-%d")

    # string to date(in format: %Y-%m-%d)
    return datetime.strptime(journey_date, "%Y-%m-%d").date()


def get_trip_list(start_station, destination, date_of_journey):
    # string is in %m/%d/%Y format
    # But we need to date in %Y-%m-%d format
    journey_date = convert_string_to_date(date_of_journey)
    trip_list = Trip.objects.filter(
        start_station__icontains=start_station,
        destination__icontains=destination,
        start_time__date=journey_date
    ).order_by('start_time__time')

    return adding_available_seat_to_trip(trip_list)


def adding_available_seat_to_trip(trip_list):
    for trip in trip_list:
        num_of_available_seats = get_num_of_available_seats(trip)
        trip.seat = num_of_available_seats
    return trip_list


def get_num_of_available_seats(trip):
    trip_seat_list = TripSeat.objects.filter(trip__id__iexact=trip.id).order_by('seat_no')
    available_seat = 0;
    for trip_seat in trip_seat_list:
        if trip_seat.status == 'AVAILABLE':
            available_seat = available_seat+ 1
    return available_seat


def get_seat_info(trip):
    trip_seat_list = TripSeat.objects.filter(trip__id__iexact=trip.id).order_by('seat_no')
    seat_info = {}
    for trip_seat in trip_seat_list:
        seat_info[trip_seat.seat_no] = trip_seat.status
    return seat_info


def thanks(request):
    return render(request, 'busTicketBooking/thanks.html')


def get_name(request):
    seat = request.GET.get('A2')

    print(seat)
    return render(request, 'busTicketBooking/thanks.html')

"""
def get_station(request):
    if request.is_ajax():
        # q = request.GET.get('term', '')
        q = 'dha'
        print('q: ' + q)
        trips = Trip.objects.filter(start_station__icontains=q).order_by('start_station')

        results = []
        for trip in trips:
            results.append(trip.start_station)
        print('result: ' + str(results))
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
"""
