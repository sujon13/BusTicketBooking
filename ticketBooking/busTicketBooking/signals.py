from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
import time
from .models import Bus, Seat, Trip, TripSeat, Reservation, ReservationSeat


@receiver(post_save, sender=Trip)
def save_seat_booking_info(sender, instance, **kwargs):
    # print(str(instance.coach_no) + ' ' + str(instance.fare))
    seat_list = Seat.objects.filter(bus__id__iexact=instance.bus.id)
    for seat in seat_list:
        obj = TripSeat(trip=instance, seat_no=seat.seat_no, status='AVAILABLE')
        obj.save()


@receiver(post_save, sender=Bus)
def save_seat_info(sender, instance, **kwargs):
    bus = instance

    for row in range(bus.num_of_rows):
        if row == 0:
            for col in range(bus.column_in_first_row):
                make_seat(bus, row, col)
        elif row == bus.num_of_rows - 1:
            for col in range(bus.column_in_last_row):
                make_seat(bus, row, col)
        else:
            for col in range(bus.num_of_columns):
                make_seat(bus, row, col)


def make_seat(bus, row_no, col_no):
    row = "ABCDEFGHIJ"
    seat_no = row[row_no] + str(col_no + 1)
    seat = Seat(bus=bus, seat_no=seat_no)
    seat.save()


@receiver(post_save, sender=Reservation)
def delete_reservation_info_after_2_min(sender, instance, **kwargs):
    # print(str(instance.coach_no) + ' ' + str(instance.fare))
    reservation = Reservation.objects.get(pk=instance.id)
    #time.sleep(10)
    #reservation.delete()
