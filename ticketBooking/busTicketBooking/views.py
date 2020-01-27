from django.shortcuts import render
from django.core.serializers import serialize
from rest_framework import serializers
from twilio.rest import Client

from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Bus, Trip, Seat, TripSeat, Passenger, Reservation, ReservationSeat
from .forms import SearchBus, PassengerInformation
from datetime import datetime


def home(request):
    # create a form instance and populate it with data from the request:
    form = SearchBus(request.GET)
    if form.is_valid():
        start_station = form.cleaned_data['start_station']
        destination = form.cleaned_data['destination']
        date_of_journey = form.cleaned_data['date_of_journey']
        trip_list = get_trip_list(start_station, destination, date_of_journey, True)
        trip_seat_list = get_trip_seat_list(trip_list)
        context = {
            'cnt': len(trip_list),
            'start_station': start_station,
            'destination': destination,
            'date_of_journey': date_of_journey,
            'trip_list': serialize('json', trip_list, use_natural_foreign_keys=True),
            'trip_seat_list': serialize('json', trip_seat_list)
        }
        return render(request, 'busTicketBooking/trip_details.html', context)

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


def get_trip_list(start_station, destination, date_of_journey, is_date_in_string_format):
    journey_date = date_of_journey
    if is_date_in_string_format:
        # string is in %m/%d/%Y format
        # But we need to date in %Y-%m-%d format
        journey_date = convert_string_to_date(date_of_journey)

    trip_list = Trip.objects.filter(
        start_station__icontains=start_station,
        destination__icontains=destination,
        start_time__date=journey_date,
        start_time__gte=datetime.now()
    ).order_by('start_time__time')
    return adding_available_seat_to_trip(trip_list)


def adding_available_seat_to_trip(trip_list):
    for trip in trip_list:
        num_of_available_seats = get_num_of_available_seats(trip)
        trip.seat = num_of_available_seats
    return trip_list


def get_num_of_available_seats(trip):
    trip_seat_list = TripSeat.objects.filter(trip__id__iexact=trip.id).order_by('seat_no')
    available_seat = 0
    for trip_seat in trip_seat_list:
        if trip_seat.status == 'AVAILABLE':
            available_seat = available_seat + 1
    return available_seat


def get_trip_seat_list(trip_list):
    trip_seat_list = []
    for trip in trip_list:
        trip_seat = TripSeat.objects.filter(trip__id__iexact=trip.id).order_by('seat_no')
        trip_seat_list.extend(trip_seat)

    return trip_seat_list
    #seat_info = {}
    #for trip_seat in trip_seat_list:
    #    seat_info[trip_seat.seat_no] = trip_seat.status
    #return seat_info


#def thanks(request):
#    return render(request, 'busTicketBooking/thanks.html')

def seat_status(request):
    try:
        #update_seat_status(request)
        print('update')
    except:
        print("error occurred in updating seat status")
    finally:
        form = PassengerInformation()
        seat_list = json.loads(request.POST.get('seat_list'))
        total_fare = request.POST.get('total_fare')
        trip_id = request.POST.get('trip_id')
        trip = Trip.objects.get(pk=trip_id)

        context = {
            'trip': trip,
            'seat_list': json.dumps(seat_list),
            'total_fare': total_fare,
            'form': form
        }
        return render(request, 'busTicketBooking/seat_booking.html', context)


def seat_booking(request):
    form = PassengerInformation(request.POST)
    seat_list = json.loads(request.POST.get('seat_list'))
    if form.is_valid():

        # save personal info
        passenger = get_passenger_info(form)
        # passenger.save()

        # save reservation info
        reservation = get_reservation_info(request, passenger, seat_list)
        #reservation.save()

        # save reservation seat info
        # save_reserved_seat_info(reservation, seat_list)

        # send sms(text message) to passenger with reservation info
        # send_sms_to_passenger(request, passenger.mobile, reservation)
        print('valid!!!')
        return render(request, 'busTicketBooking/home.html')
    else:
        print('invalid!!')
        total_fare = request.POST.get('total_fare')
        trip_id = request.POST.get('trip_id')
        trip = Trip.objects.get(pk=trip_id)

        context = {
            'trip': trip,
            'seat_list': json.dumps(seat_list),
            'total_fare': total_fare,
            'form': form
        }
        return render(request, 'busTicketBooking/seat_booking.html', context)


def get_reservation_info(request, passenger, seat_list):
    num_of_booked_seat = len(seat_list)
    total_payable_fee = int(request.POST.get('total_payable_fee'))
    trip_id = request.POST.get('trip_id')
    trip = Trip.objects.get(pk=trip_id)
    reservation = Reservation(
        trip=trip,
        passenger=passenger,
        reservation_time=datetime.now(),
        num_of_booked_seat=num_of_booked_seat,
        total_fare=total_payable_fee
    )
    return reservation


def update_seat_status(request):
    trip_id = request.POST.get('trip_id')
    seat_list = json.loads(request.POST.get('seat_list'))
    print(seat_list)

    # these seats are booked. we need to update trip-seat table of database
    for seat in seat_list:
        TripSeat.objects.filter(
           trip__id__iexact=trip_id,
           seat_no__iexact=seat
        ).update(status='BOOKED')


def get_passenger_info(form):
    name = form.cleaned_data['name']
    gender = form.cleaned_data['gender']
    mobile = form.cleaned_data['mobile']
    email = form.cleaned_data['email']
    passenger = Passenger(
        name=name,
        gender=gender,
        mobile=mobile,
        email=email
    )
    return passenger


def save_reserved_seat_info(reservation, seat_list):
    for seat in seat_list:
        reserved_seat = ReservationSeat(
            reservation=reservation,
            seat_no=seat
        )
        reserved_seat.save()


def send_sms_to_passenger(request, mobile, reservation):
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = 'AC94bf58b42dfc88ce7a5ff6d01cbbf4ea'
    auth_token = 'af7ab3de8a20e70fd4cc90f173a2026b'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=get_sms_body(request, reservation),
        from_='+13143154321',
        status_callback='https://d361e169.ngrok.io/busTicketBooking/seat_booking/sms-status/',
        to=str(mobile)
    )
    print(message.sid)


def get_sms_body(request, reservation):
    trip_id = request.POST.get('trip_id')
    trip = Trip.objects.get(pk=trip_id)
    sms_body = 'bKash Reservation Confirmation ' + trip.start_station.capitalize()\
               + ' to ' + trip.destination.capitalize()
    sms_body += '. Reservation Reference: ' + str(reservation.id * 10)
    sms_body += '. Please confirm bKash Payment of BDT. ' + str(reservation.total_fare) + ' within 20 minutes'
    return sms_body


@csrf_exempt
def sms_status(request):
    print('in here!')
    SmsSid = request.POST.get('SmsSid')
    SmsStatus = request.POST.get('SmsStatus')
    To = request.POST.get('To')
    if SmsStatus == 'sent' or SmsStatus == 'delivered':
        print('successfully sent message')
    else:
        print('Error occurred. Steps need to be taken')

    return render(request, 'busTicketBooking/home.html')

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
