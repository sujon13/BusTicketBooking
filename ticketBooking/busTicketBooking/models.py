from django.db import models
from datetime import datetime


class Bus(models.Model):
    operator_name = models.CharField(max_length=20)
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
    total_seat = models.IntegerField(default=40)

    def __str__(self):
        return self.operator_name + ' ' + self.manufacturer


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
        return self.start_station + '-' + self.end_station + ' ' + self.start_time.strftime("%B %d, %Y %H:%M")

