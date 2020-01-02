from django.apps import AppConfig


class BusticketbookingConfig(AppConfig):
    name = 'busTicketBooking'

    def ready(self):
        import busTicketBooking.signals