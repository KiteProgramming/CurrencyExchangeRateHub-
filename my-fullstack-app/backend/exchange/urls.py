from django.urls import path
from .views import update_credentials, CurrencyExchangeRateListCreate, manual_sync, CurrencyListCreate, add_exchange_rate, update_exchange_rate, delete_exchange_rate, update_currency, delete_currency

urlpatterns = [
    path('update-credentials/', update_credentials, name='update_credentials'),
    path('exchange-rates/', CurrencyExchangeRateListCreate.as_view(), name='exchange_rates'),    
    path('manual-sync/', manual_sync, name='manual_sync'),
    path('currencies/', CurrencyListCreate.as_view(), name='currencies'),
    path('add-exchange-rate/', add_exchange_rate, name='add-exchange-rate'),
    path('update-exchange-rate/<str:pair>/', update_exchange_rate, name='update-exchange-rate'),
    path('delete-exchange-rate/<str:pair>/', delete_exchange_rate, name='delete-exchange-rate'),
    path('update-currency/<str:code>/', update_currency, name='update-currency'),
    path('delete-currency/<str:code>/', delete_currency, name='delete-currency'),
]