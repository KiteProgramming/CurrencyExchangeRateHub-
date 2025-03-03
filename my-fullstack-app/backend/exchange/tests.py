from django.test import TestCase
from .models import Currency, CurrencyExchangeRate
from .tasks import fetch_exchange_rates, the_manual_sync
from unittest.mock import patch, MagicMock
from decimal import Decimal

class CurrencyModelTest(TestCase):

    def setUp(self):
        Currency.objects.create(code='USD', name='United States Dollar')
        Currency.objects.create(code='EUR', name='Euro')

    def test_currency_creation(self):
        usd = Currency.objects.get(code='USD')
        eur = Currency.objects.get(code='EUR')
        self.assertEqual(usd.name, 'United States Dollar')
        self.assertEqual(eur.name, 'Euro')

class CurrencyExchangeRateTest(TestCase):

    def setUp(self):
        self.usd = Currency.objects.create(code='USD', name='United States Dollar')
        self.eur = Currency.objects.create(code='EUR', name='Euro')
        self.gbp = Currency.objects.create(code='GBP', name='British Pound')
        self.exchange_rate_usd_eur = CurrencyExchangeRate.objects.create(pair='USD-EUR', rate=Decimal('0.850000'))
        self.exchange_rate_usd_gbp = CurrencyExchangeRate.objects.create(pair='USD-GBP', rate=Decimal('0.750000'))

    def test_exchange_rate_creation(self):
        exchange_rate = CurrencyExchangeRate.objects.get(pair='USD-EUR')
        self.assertEqual(exchange_rate.rate, Decimal('0.850000'))

    def test_add_exchange_rate(self):
        new_rate = CurrencyExchangeRate.objects.create(pair='USD-JPY', rate=Decimal('110.000000'))
        self.assertEqual(new_rate.rate, Decimal('110.000000'))

    @patch('exchange.tasks.requests.get')
    def test_fetch_exchange_rates_xe(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'to': [
                {'quotecurrency': 'EUR', 'mid': 0.85},
                {'quotecurrency': 'GBP', 'mid': 0.75}
            ]
        }
        mock_get.return_value = mock_response

        fetch_exchange_rates(api_choice='XE')

        usd_eur = CurrencyExchangeRate.objects.get(pair='USD-EUR')
        usd_gbp = CurrencyExchangeRate.objects.get(pair='USD-GBP')

        self.assertEqual(usd_eur.rate, Decimal('0.850000'))
        self.assertEqual(usd_gbp.rate, Decimal('0.750000'))

    @patch('exchange.tasks.requests.get')
    def test_fetch_exchange_rates_exchangerate_api(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'conversion_rates': {
                'EUR': 0.85,
                'GBP': 0.75
            }
        }
        mock_get.return_value = mock_response

        fetch_exchange_rates(api_choice='ExchangeRate-API')

        usd_eur = CurrencyExchangeRate.objects.get(pair='USD-EUR')
        usd_gbp = CurrencyExchangeRate.objects.get(pair='USD-GBP')

        self.assertEqual(usd_eur.rate, Decimal('0.850000'))
        self.assertEqual(usd_gbp.rate, Decimal('0.750000'))