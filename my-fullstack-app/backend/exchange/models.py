from django.db import models
from .fields import EncryptedCharField

class CurrencyExchangeRate(models.Model):
    currency = models.CharField(max_length=10)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.currency}: {self.rate}"

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
    interval_minutes = models.IntegerField(default=60)  # Interval for scheduler in minutes

    def __str__(self):
        return self.code