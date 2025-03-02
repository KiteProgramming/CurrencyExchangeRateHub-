from django import forms
from .models import XECredentials

class XECredentialsForm(forms.ModelForm):
    class Meta:
        model = XECredentials
        fields = ['api_key', 'api_secret']