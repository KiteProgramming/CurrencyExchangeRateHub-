from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect, get_object_or_404
from .models import XECredentials, ExchangeRateAPICredentials, Currency, CurrencyExchangeRate
from .forms import XECredentialsForm, ExchangeRateAPICredentialsForm
from rest_framework import generics
from .serializers import CurrencyExchangeRateSerializer, CurrencySerializer
from .tasks import fetch_exchange_rates, the_manual_sync
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

class CurrencyExchangeRateListCreate(generics.ListCreateAPIView):
    queryset = CurrencyExchangeRate.objects.all()
    serializer_class = CurrencyExchangeRateSerializer

def update_credentials(request):
    xe_credentials = XECredentials.objects.first()
    exchange_rate_api_credentials = ExchangeRateAPICredentials.objects.first()
    
    if request.method == 'POST':
        xe_form = XECredentialsForm(request.POST, instance=xe_credentials)
        exchange_rate_api_form = ExchangeRateAPICredentialsForm(request.POST, instance=exchange_rate_api_credentials)
        
        if xe_form.is_valid() and exchange_rate_api_form.is_valid():
            xe_form.save()
            exchange_rate_api_form.save()
            return redirect('update_credentials')
    else:
        xe_form = XECredentialsForm(instance=xe_credentials)
        exchange_rate_api_form = ExchangeRateAPICredentialsForm(instance=exchange_rate_api_credentials)
    
    return render(request, 'update_credentials.html', {'xe_form': xe_form, 'exchange_rate_api_form': exchange_rate_api_form})

def view_credentials(request):
    xe_credentials = XECredentials.objects.first()
    exchange_rate_api_credentials = ExchangeRateAPICredentials.objects.first()
    return render(request, 'exchange/view_credentials.html', {'xe_credentials': xe_credentials, 'exchange_rate_api_credentials': exchange_rate_api_credentials})

def manual_sync(request):
    api_choice = request.GET.get('api_choice', 'XE')
    if api_choice == 'ExchangeRate-API':
        the_manual_sync(api_choice='ExchangeRate-API')
    else:
        the_manual_sync(api_choice='XE')
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

@csrf_exempt
@require_http_methods(["PUT"])
def update_exchange_rate(request, pair):
    data = json.loads(request.body)
    rate = data.get('rate')

    if rate is None:
        return JsonResponse({'error': 'Rate is required'}, status=400)

    exchange_rate = get_object_or_404(CurrencyExchangeRate, pair=pair)
    exchange_rate.rate = rate
    exchange_rate.save()

    return JsonResponse({'pair': exchange_rate.pair, 'rate': exchange_rate.rate, 'updated_at': exchange_rate.updated_at})

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_exchange_rate(request, pair):
    exchange_rate = get_object_or_404(CurrencyExchangeRate, pair=pair)
    exchange_rate.delete()
    return JsonResponse({'message': 'Exchange rate deleted successfully'}, status=204)

@csrf_exempt
@require_http_methods(["PUT"])
def update_currency(request, code):
    data = json.loads(request.body)
    new_code = data.get('code')
    new_name = data.get('name')

    if new_code is None or new_name is None:
        return JsonResponse({'error': 'Code and name are required'}, status=400)

    currency = get_object_or_404(Currency, code=code)
    currency.code = new_code
    currency.name = new_name
    currency.save()

    return JsonResponse({'code': currency.code, 'name': currency.name})

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_currency(request, code):
    currency = get_object_or_404(Currency, code=code)
    currency.delete()
    return JsonResponse({'message': 'Currency deleted successfully'}, status=204)