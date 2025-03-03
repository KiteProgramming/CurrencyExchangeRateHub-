from django.apps import AppConfig
import sys

class ExchangeConfig(AppConfig):
    name = 'exchange'

    def ready(self):
        if 'runserver' in sys.argv or 'runserver_plus' in sys.argv:
            from .scheduler import start
            start()