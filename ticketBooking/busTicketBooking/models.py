from django.db import models
from datetime import datetime


class Seat(models.Model):
    total_seat = models.IntegerField(default=40)
    num_of_rows = models.IntegerField(default=10)
    num_of_columns = models.IntegerField(default=4)
    column_in_first_row = models.IntegerField(default=4)
    column_in_last_row = models.IntegerField(default=5)

    SEAT_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('BOOKED', 'Booked'),
        ('SOLD', 'Sold'),
        ('DISABLED', 'Disabled')
    ]
    A1 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    A2 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    A3 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    A4 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')

    B1 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    B2 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    B3 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    B4 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')

    C1 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    C2 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    C3 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    C4 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')

    D1 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    D2 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    D3 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    D4 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')

    E1 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    E2 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    E3 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    E4 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')

    F1 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    F2 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    F3 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    F4 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')

    G1 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    G2 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    G3 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    G4 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')

    H1 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    H2 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    H3 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    H4 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')

    I1 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    I2 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    I3 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    I4 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')

    J1 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    J2 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    J3 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    J4 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')
    J5 = models.CharField(max_length=10, choices=SEAT_CHOICES, default='AVAILABLE')

    def __str__(self):
        return str(self.total_seat)


class Bus(models.Model):
    operator_name = models.CharField(max_length=20)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, null=True, blank=True)
    MANUFACTURER_CHOICES = [
        ('SCANIA', 'Scania'),
        ('VOLVO', 'Volvo'),
        ('HYUNDAI', 'Hyundai'),
        ('HINO', 'Hino'),
        ('MAN', 'Man'),
    ]
    manufacturer = models.CharField(max_length=10, choices=MANUFACTURER_CHOICES, default='HINO')

    CLASS_CHOICES = [
        ('ECONOMY', 'Economy Class'),
        ('BUSINESS', 'Business Class')
    ]
    Class = models.CharField(max_length=10, choices=CLASS_CHOICES, default='ECONOMY')

    hasAc = models.BooleanField(default=True)

    def __str__(self):
        ret = self.operator_name + ' ' + self.manufacturer + ' '
        extra_information = 'AC' if self.hasAc is True else 'Non AC'
        ret = ret + extra_information + ' '
        extra_information = '(E)' if self.Class == 'ECONOMY' else '(B)'
        return ret + extra_information


class Trip(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)

    START_STATION_CHOICES = [
        ('DHAKA', 'Dhaka'),
        ('CHATTAGRAM', 'Chattagram'),
        ('BARISAL', 'Barisal'),
        ('SYLHET', 'Sylhet'),
        ('KHULNA', 'Khulna'),
    ]
    start_station = models.CharField(max_length=20, choices=START_STATION_CHOICES, default='...')

    END_STATION_CHOICES = [
        ('DHAKA', 'Dhaka'),
        ('CHATTAGRAM', 'Chattagram'),
        ('BARISAL', 'Barisal'),
        ('SYLHET', 'Sylhet'),
        ('KHULNA', 'Khulna'),
    ]
    end_station = models.CharField(max_length=20, choices=END_STATION_CHOICES, default='...')

    coachNo = models.IntegerField(null=True)
    fare = models.IntegerField(default=0)
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.TimeField(null=True, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        ret = self.start_station + '-' + self.end_station + ' '
        ret = ret + '(' + self.bus.operator_name + ')' + ' '
        return ret + self.start_time.strftime("%B %d, %Y %H:%M")

