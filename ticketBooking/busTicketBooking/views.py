from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Bus, Trip
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
def get_trip_list(start_station, end_station, date_of_journey):
    # date to string
    date_of_journey = datetime.strftime(date_of_journey, '%Y-%m-%d')
    # string to date
    journey_date = datetime.strptime(date_of_journey, "%Y-%m-%d").date()

    trip_list = Trip.objects.filter(start_station__icontains=start_station,
                                    end_station__icontains=end_station,
                                    start_time__date=journey_date)
    return trip_list


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
