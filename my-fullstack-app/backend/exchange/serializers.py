from rest_framework import serializers
from .models import CurrencyExchangeRate, Currency

class CurrencyExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyExchangeRate
        fields = ['id', 'currency', 'rate', 'created_at', 'updated_at']

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'code', 'name', 'interval_minutes']