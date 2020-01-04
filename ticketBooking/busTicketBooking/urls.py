from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('<int:bus_id>/', views.seat, name='seat'),
    path('thanks/nameForm/', views.get_name, name='get_name'),
    # path('thanks/', views.thanks, name='thanks'),
    # path('api/get_station/', views.get_station, name='get_station'),
]
