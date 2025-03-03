from django.db import models
from .fields import EncryptedCharField

class CurrencyExchangeRate(models.Model):
    pair = models.CharField(max_length=7, unique=True)  # e.g., "USD-EUR"
    rate = models.DecimalField(max_digits=20, decimal_places=6)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pair}: {self.rate}"

class XECredentials(models.Model):
    api_key = EncryptedCharField(max_length=255)
    api_secret = EncryptedCharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.api_key

    class Meta:
        verbose_name = "XE Credential"
        verbose_name_plural = "XE Credentials"

class Currency(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.code