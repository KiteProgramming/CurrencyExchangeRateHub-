from django import forms
from .models import XECredentials, ExchangeRateAPICredentials

class XECredentialsForm(forms.ModelForm):
    class Meta:
        model = XECredentials
        fields = ['xe_api_key', 'api_secret']

class ExchangeRateAPICredentialsForm(forms.ModelForm):
    class Meta:
        model = ExchangeRateAPICredentials
        fields = ['api_key']