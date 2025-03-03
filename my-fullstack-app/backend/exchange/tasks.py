import requests
import logging
from django.conf import settings
from .models import XECredentials, Currency, CurrencyExchangeRate
from background_task import background

logger = logging.getLogger('django')

@background(schedule=60)
def fetch_exchange_rates():
    logger.debug("Starting fetch_exchange_rates task")
    _fetch_exchange_rates()

def _fetch_exchange_rates():
    logger.debug("Starting _fetch_exchange_rates function")
    credentials = XECredentials.objects.first()
    logger.debug(f"Credentials: {credentials}")
    if not credentials:
        logger.error("No credentials found")
        return

    try:
        # Directly use the decrypted API key and secret
        api_key = credentials.api_key
        api_secret = credentials.api_secret
        logger.debug(f"API Key: {api_key}")
        logger.debug(f"API Secret: {api_secret}")
    except Exception as e:
        logger.error(f"Error processing credentials: {e}")
        return

    currencies = Currency.objects.all()
    logger.debug(f"Currencies: {currencies}")
    for from_currency in currencies:
        to_currencies = ','.join([c.code for c in currencies if c.code != from_currency.code])
        url = f"https://xecdapi.xe.com/v1/convert_from?from={from_currency.code}&to={to_currencies}"
        logger.debug(f"Request URL: {url}")
        response = requests.get(url, auth=(api_key, api_secret))
        logger.debug(f"Response Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            logger.debug(f"Response Data: {data}")
            for rate in data['to']:
                pair = f"{from_currency.code}-{rate['quotecurrency']}"
                CurrencyExchangeRate.objects.update_or_create(
                    pair=pair,
                    defaults={'rate': rate['mid']}
                )
                logger.debug(f"Updated rate for {pair}: {rate['mid']}")
        else:
            logger.error(f"Error fetching exchange rates: {response.status_code} - {response.text}")

# Schedule the task to run every 60 seconds
def schedule_fetch_exchange_rates():
    currencies = Currency.objects.all()
    for currency in currencies:
        fetch_exchange_rates(repeat=3600 * 60)

# Manual sync function
def the_manual_sync():
    logger.debug("Starting manual_sync function")
    _fetch_exchange_rates()