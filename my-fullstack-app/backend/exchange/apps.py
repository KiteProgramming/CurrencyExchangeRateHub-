from django.apps import AppConfig

class ExchangeConfig(AppConfig):
    name = 'exchange'

    def ready(self):
        from .tasks import schedule_fetch_exchange_rates
        schedule_fetch_exchange_rates()