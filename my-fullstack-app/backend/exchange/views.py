from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from .models import XECredentials, Currency
from .forms import XECredentialsForm
from rest_framework import generics
from .models import CurrencyExchangeRate
from .serializers import CurrencyExchangeRateSerializer, CurrencySerializer
from .tasks import fetch_exchange_rates, the_manual_sync, schedule_fetch_exchange_rates
from django.http import HttpResponse , JsonResponse

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
    the_manual_sync()
    return JsonResponse({"status": "Manual sync initiated"})


class CurrencyListCreate(generics.ListCreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

@api_view(['POST'])
def add_exchange_rate(request):
    pair = request.data.get('pair')
    rate = request.data.get('rate')
    
    if not pair or not rate:
        return Response({'error': 'Pair and rate are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    exchange_rate, created = CurrencyExchangeRate.objects.update_or_create(
        pair=pair,
        defaults={'rate': rate}
    )
    
    serializer = CurrencyExchangeRateSerializer(exchange_rate)
    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)    
