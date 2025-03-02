from django.shortcuts import render, redirect
from .models import XECredentials, Currency
from .forms import XECredentialsForm
from rest_framework import generics
from .models import CurrencyExchangeRate
from .serializers import CurrencyExchangeRateSerializer, CurrencySerializer
from .tasks import fetch_exchange_rates, schedule_fetch_exchange_rates

class CurrencyExchangeRateListCreate(generics.ListCreateAPIView):
    queryset = CurrencyExchangeRate.objects.all()
    serializer_class = CurrencyExchangeRateSerializer

def update_credentials(request):
    credentials = XECredentials.objects.first()
    if request.method == 'POST':
        form = XECredentialsForm(request.POST, instance=credentials)
        if form.is_valid():
            form.save()
            return redirect('update_credentials')
    else:
        form = XECredentialsForm(instance=credentials)
    return render(request, 'update_credentials.html', {'form': form})

def view_credentials(request):
    credentials = XECredentials.objects.first()
    return render(request, 'exchange/view_credentials.html', {'credentials': credentials})

def manual_sync(request):    
    fetch_exchange_rates()
    #return redirect('update_credentials')


class CurrencyListCreate(generics.ListCreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
