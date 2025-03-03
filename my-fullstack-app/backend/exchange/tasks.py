import requests
import logging
from django.conf import settings
from .models import XECredentials, Currency, CurrencyExchangeRate, ExchangeRateAPICredentials
from background_task import background, tasks

logger = logging.getLogger('django')

@background(schedule=60)
def fetch_exchange_rates(api_choice='XE'):
    logger.debug("Starting fetch_exchange_rates task")
    primary_success = False

    if api_choice == 'ExchangeRate-API':
        primary_success = _fetch_exchange_rates_exchangerate_api()
        if not primary_success:
            logger.debug("Primary API failed, attempting fallback to XE API")
            _fetch_exchange_rates_xe()
        else:
            logger.debug("Primary API succeeded, no need to fallback")    
    else:
        primary_success = _fetch_exchange_rates_xe()
        logger.debug(f"primary_success: {primary_success}")
        if not primary_success:
            logger.debug("Primary API failed, attempting fallback to ExchangeRate-API")
            _fetch_exchange_rates_exchangerate_api()
        else:
            logger.debug("Primary API succeeded, no need to fallback")    

def _fetch_exchange_rates_xe():
    logger.debug("Starting _fetch_exchange_rates_xe function")
    credentials = XECredentials.objects.first()
    logger.debug(f"Credentials: {credentials}")
    if not credentials:
        logger.error("No credentials found")
        return False

    try:
        xe_api_key = credentials.xe_api_key
        api_secret = credentials.api_secret
        logger.debug(f"API Key: {xe_api_key}")
        logger.debug(f"API Secret: {api_secret}")
    except Exception as e:
        logger.error(f"Error processing credentials: {e}")
        return False

    currencies = Currency.objects.all()
    logger.debug(f"Currencies: {currencies}")
    for from_currency in currencies:
        to_currencies = ','.join([c.code for c in currencies if c.code != from_currency.code])
        url = f"https://xecdapi.xe.com/v1/convert_from?from={from_currency.code}&to={to_currencies}"
        logger.debug(f"Request URL: {url}")
        response = requests.get(url, auth=(xe_api_key, api_secret))
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
            return False
    return True

def _fetch_exchange_rates_exchangerate_api():
    logger.debug("Starting _fetch_exchange_rates_exchangerate_api function")
    credentials = ExchangeRateAPICredentials.objects.first()
    logger.debug(f"Credentials: {credentials}")
    if not credentials:
        logger.error("No credentials found")
        return False

    try:
        api_key = credentials.api_key
        logger.debug(f"API Key: {api_key}")
    except Exception as e:
        logger.error(f"Error processing credentials: {e}")
        return False

    try:
        currencies = Currency.objects.all()
        logger.debug(f"Currencies: {currencies}")
        for from_currency in currencies:
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency.code}"
            logger.debug(f"Request URL: {url}")
            response = requests.get(url)
            logger.debug(f"Response Status Code: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                logger.debug(f"Response Data: {data}")
                for to_currency, rate in data['conversion_rates'].items():
                    if to_currency != from_currency.code and Currency.objects.filter(code=to_currency).exists():
                        pair = f"{from_currency.code}-{to_currency}"
                        CurrencyExchangeRate.objects.update_or_create(
                            pair=pair,
                            defaults={'rate': rate}
                        )
                        logger.debug(f"Updated rate for {pair}: {rate}")
            else:
                logger.error(f"Error fetching exchange rates: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        logger.error(f"Error processing exchange rates: {e}")
        return False
    return True

# Manual sync function
def the_manual_sync(api_choice='XE'):
    logger.debug("Starting manual_sync function")
    if api_choice == 'ExchangeRate-API':
        _fetch_exchange_rates_exchangerate_api()
    else:
        _fetch_exchange_rates_xe()