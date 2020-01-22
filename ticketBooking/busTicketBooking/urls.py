from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('<int:bus_id>/', views.seat, name='seat'),
    path('seat_status/', views.seat_status, name='seat_status'),
    path('seat_booking/', views.seat_booking, name='seat_booking'),
    # path('thanks/', views.thanks, name='thanks'),
    # path('api/get_station/', views.get_station, name='get_station'),
    path('seat_booking/sms-status/', views.sms_status, name='sms_status'),
]