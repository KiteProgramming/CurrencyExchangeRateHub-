from django.test import TestCase
from .models import Currency

class CurrencyModelTest(TestCase):

    def setUp(self):
        Currency.objects.create(code='USD', name='United States Dollar')
        Currency.objects.create(code='EUR', name='Euro')

    def test_currency_creation(self):
        usd = Currency.objects.get(code='USD')
        eur = Currency.objects.get(code='EUR')
        self.assertEqual(usd.name, 'United States Dollar')
        self.assertEqual(eur.name, 'Euro')