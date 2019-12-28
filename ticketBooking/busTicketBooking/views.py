from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import  json
from .models import Bus, Trip, Seat
from .forms import NameForm, SearchBus
from datetime import datetime


def home(request):
    # create a form instance and populate it with data from the request:
    form = SearchBus(request.GET)
    if form.is_valid():
        start_station = form.cleaned_data['start_station']
        end_station = form.cleaned_data['end_station']
        date_of_journey = form.cleaned_data['date_of_journey']
        trip_list = get_trip_list(start_station, end_station, date_of_journey)

        context = {'number_of_buses': trip_list.count(), 'tripList': trip_list}
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


def get_trip_list(start_station, end_station, date_of_journey):
    # string is in %m/%d/%Y format
    # But we need to date in %Y-%m-%d format
    journey_date = convert_string_to_date(date_of_journey)
    trip_list = Trip.objects.filter(
        start_station__icontains=start_station,
        end_station__icontains=end_station,
        start_time__date=journey_date
    ).order_by('start_time__time')

    return adding_available_seat_to_trip(trip_list)


def adding_available_seat_to_trip(trip_list):
    for trip in trip_list:
        num_of_available_seats = get_num_of_available_seats(trip.bus.seat.id)
        trip.seat = num_of_available_seats
    return trip_list


def get_num_of_available_seats(seat_id):
    seat = Seat.objects.get(pk=seat_id)
    num = 0
    if seat.A1 == 'AVAILABLE':
        num += 1
    if seat.A2 == 'AVAILABLE':
        num += 1
    if seat.A3 == 'AVAILABLE':
        num += 1
    if seat.A4 == 'AVAILABLE':
        num += 1

    if seat.B1 == 'AVAILABLE':
        num += 1
    if seat.B2 == 'AVAILABLE':
        num += 1
    if seat.B3 == 'AVAILABLE':
        num += 1
    if seat.B4 == 'AVAILABLE':
        num += 1

    if seat.C1 == 'AVAILABLE':
        num += 1
    if seat.C2 == 'AVAILABLE':
        num += 1
    if seat.C3 == 'AVAILABLE':
        num += 1
    if seat.C4 == 'AVAILABLE':
        num += 1

    if seat.D1 == 'AVAILABLE':
        num += 1
    if seat.D2 == 'AVAILABLE':
        num += 1
    if seat.D3 == 'AVAILABLE':
        num += 1
    if seat.D4 == 'AVAILABLE':
        num += 1

    if seat.E1 == 'AVAILABLE':
        num += 1
    if seat.E2 == 'AVAILABLE':
        num += 1
    if seat.E3 == 'AVAILABLE':
        num += 1
    if seat.E4 == 'AVAILABLE':
        num += 1

    if seat.F1 == 'AVAILABLE':
        num += 1
    if seat.F2 == 'AVAILABLE':
        num += 1
    if seat.F3 == 'AVAILABLE':
        num += 1
    if seat.F4 == 'AVAILABLE':
        num += 1

    if seat.G1 == 'AVAILABLE':
        num += 1
    if seat.G2 == 'AVAILABLE':
        num += 1
    if seat.G3 == 'AVAILABLE':
        num += 1
    if seat.G4 == 'AVAILABLE':
        num += 1

    if seat.H1 == 'AVAILABLE':
        num += 1
    if seat.H2 == 'AVAILABLE':
        num += 1
    if seat.H3 == 'AVAILABLE':
        num += 1
    if seat.H4 == 'AVAILABLE':
        num += 1

    if seat.I1 == 'AVAILABLE':
        num += 1
    if seat.I2 == 'AVAILABLE':
        num += 1
    if seat.I3 == 'AVAILABLE':
        num += 1
    if seat.I4 == 'AVAILABLE':
        num += 1

    if seat.J1 == 'AVAILABLE':
        num += 1
    if seat.J2 == 'AVAILABLE':
        num += 1
    if seat.J3 == 'AVAILABLE':
        num += 1
    if seat.J4 == 'AVAILABLE':
        num += 1
    if seat.J5 == 'AVAILABLE':
        num += 1

    return num


def seat(request, bus_id):
    seats = Bus.objects.get(pk=bus_id).seat
    context = {'seat': seats}
    return render(request, 'busTicketBooking/seat.html', context)


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # return HttpResponseRedirect('thanks')
            context = {'name': form.cleaned_data['name']}
            return render(request, 'busTicketBooking/thanks.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'busTicketBooking/name.html', {'form': form})


def thanks(request):
    return render(request, 'busTicketBooking/thanks.html')


def get_station(request):
    if request.is_ajax():
        # q = request.GET.get('term', '')
        q = 'dha'
        print('q: ' + q)
        trips = Trip.objects.filter(start_station__icontains=q).order_by('start_station')


        # stations.append(Trip.objects.filter(end_station__icontains=q))
        results = []
        for trip in trips:
            results.append(trip.start_station)
        print('result: ' + str(results))
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
