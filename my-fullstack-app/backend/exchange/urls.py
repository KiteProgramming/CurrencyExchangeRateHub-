from django.urls import path
from .views import update_credentials, CurrencyExchangeRateListCreate, manual_sync, CurrencyListCreate, add_exchange_rate

urlpatterns = [
    path('update-credentials/', update_credentials, name='update_credentials'),
    path('exchange-rates/', CurrencyExchangeRateListCreate.as_view(), name='exchange_rates'),    
    path('manual-sync/', manual_sync, name='manual_sync'),
    path('currencies/', CurrencyListCreate.as_view(), name='currencies'),
    path('add-exchange-rate/', add_exchange_rate, name='add-exchange-rate'),
]