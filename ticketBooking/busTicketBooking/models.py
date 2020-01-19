from django.db import models
from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField


class Bus(models.Model):
    OPERATOR_CHOICES = [
        ('Hanif', 'Hanif'),
        ('Green Line', 'Green Line'),
        ('Tungipara Express', 'Tungipara Express'),
        ('Saintmartin Hyundai', 'Saintmartin Hyundai')
    ]
    operator_name = models.CharField(max_length=50, choices=OPERATOR_CHOICES, default='...')

    MANUFACTURER_CHOICES = [
        ('SCANIA', 'Scania'),
        ('VOLVO', 'Volvo'),
        ('HYUNDAI', 'Hyundai'),
        ('HINO', 'Hino'),
        ('MAN', 'Man')
    ]
    manufacturer = models.CharField(max_length=50, choices=MANUFACTURER_CHOICES, default='HINO')

    CLASS_CHOICES = [
        ('ECONOMY', 'Economy Class'),
        ('BUSINESS', 'Business Class')
    ]
    Class = models.CharField(max_length=10, choices=CLASS_CHOICES, default='ECONOMY')

    hasAc = models.BooleanField(default=True)
    total_seat = models.IntegerField(default=40)
    num_of_rows = models.IntegerField(default=10)
    num_of_columns = models.IntegerField(default=4)
    column_in_first_row = models.IntegerField(default=4)
    column_in_last_row = models.IntegerField(default=5)

    def get_rows(self):
        rows = "ABCDEFGHI"
        if self.num_of_rows == 10:
            rows = rows + "J"
        return rows

    def natural_key(self):
        return (self.operator_name, self.manufacturer, self.hasAc, self.total_seat, self.num_of_rows,
                self.num_of_columns, self.column_in_first_row, self.column_in_last_row)

    def __str__(self):
        ret = self.operator_name + ' ' + self.manufacturer + ' '
        extra_information = 'AC' if self.hasAc is True else 'Non AC'
        ret = ret + extra_information + ' '
        extra_information = '(E)' if self.Class == 'ECONOMY' else '(B)'
        return ret + extra_information


class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, null=True, blank=True)
    seat_no = models.CharField(max_length=50, default="A1")

    def __str__(self):
        ret = self.bus.operator_name + ' ' + self.bus.manufacturer + ' '
        extra_information = 'AC' if self.bus.hasAc is True else 'Non AC'
        ret = ret + extra_information + ' '
        extra_information = '(E)' if self.bus.Class == 'ECONOMY' else '(B)'
        return ret + extra_information + ' ' + self.seat_no


class Trip(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, null=True, blank=True)
    coach_no = models.IntegerField(default=100)
    START_STATION_CHOICES = [
        ('DHAKA', 'Dhaka'),
        ('CHATTAGRAM', 'Chattagram'),
        ('BARISAL', 'Barisal'),
        ('SYLHET', 'Sylhet'),
        ('KHULNA', 'Khulna'),
    ]
    start_station = models.CharField(max_length=50, choices=START_STATION_CHOICES, default='...')

    DESTINATION_CHOICES = [
        ('DHAKA', 'Dhaka'),
        ('CHATTAGRAM', 'Chattagram'),
        ('BARISAL', 'Barisal'),
        ('SYLHET', 'Sylhet'),
        ('KHULNA', 'Khulna'),
    ]
    destination = models.CharField(max_length=50, choices=DESTINATION_CHOICES, default='...')

    fare = models.IntegerField(default=0)
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.TimeField(null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        ret = str(self.id) + ' ' + self.start_station + '-' + self.destination + ' '
        ret = ret + '(' + self.bus.operator_name + ')' + ' '
        return ret + self.start_time.strftime("%B %d, %Y %H:%M")


class TripSeat(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    seat_no = models.CharField(max_length=50)

    SEAT_STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('SOLD', 'Sold'),
        ('BOOKED', 'Booked'),
        ('DISABLED', 'Disabled'),
    ]
    status = models.CharField(max_length=50, choices=SEAT_STATUS_CHOICES, default='...')

    def natural_key(self):
        return(self.trip.id, self.seat_no, self.status)

    def __str__(self):
        return str(self.trip) + ' ' + str(self.seat_no) + ' ' + self.status


class Passenger(models.Model):
    name = models.CharField(max_length=20)

    GENDER_CHOICES = [
        ('MALE', 'M'),
        ('FEMALE', 'F'),
        ('OTHER', 'O'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    mobile = PhoneNumberField(null=False, blank=False, region="BD")
    email = models.EmailField(max_length=50)


class Reservation(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    reservation_time = models.DateTimeField(default=datetime.now)
    num_of_booked_seat = models.IntegerField(default=1)
    total_fare = models.IntegerField(default=0)


class ReservationSeat(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    seat_no = models.CharField(max_length=10)