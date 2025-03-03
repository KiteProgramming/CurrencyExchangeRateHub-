from django.contrib import admin
from .models import XECredentials , ExchangeRateAPICredentials

admin.site.register(XECredentials)
admin.site.register(ExchangeRateAPICredentials)