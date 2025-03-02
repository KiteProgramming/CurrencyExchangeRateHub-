import requests
from django.conf import settings
from .models import XECredentials, Currency, CurrencyExchangeRate
from background_task import background
from cryptography.fernet import Fernet

@background(schedule=60)
def fetch_exchange_rates():
    credentials = XECredentials.objects.first()
    print(credentials)
    if not credentials:
        return

    api_key = Fernet(settings.ENCRYPTION_KEY).decrypt(credentials.api_key.encode()).decode()
    api_secret = Fernet(settings.ENCRYPTION_KEY).decrypt(credentials.api_secret.encode()).decode()
    print(api_key)
    print(api_secret)
    currencies = Currency.objects.all()
    for currency in currencies:
        from_currency = currency.code
        to_currencies = ','.join([c.code for c in currencies if c.code != from_currency])
        url = f"https://xecdapi.xe.com/v1/convert_from?from={from_currency}&to={to_currencies}"
        response = requests.get(url, auth=(api_key, api_secret))
        if response.status_code == 200:
            data = response.json()
            for rate in data['to']:
                CurrencyExchangeRate.objects.update_or_create(
                    currency=rate['quotecurrency'],
                    defaults={'rate': rate['mid']}
                )

# Schedule the task to run at the specified interval
def schedule_fetch_exchange_rates():
    currencies = Currency.objects.all()
    for currency in currencies:
        fetch_exchange_rates(repeat=currency.interval_minutes * 60)