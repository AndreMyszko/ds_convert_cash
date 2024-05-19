import requests


def get_coingecko_values():
    try:
        # Make a GET request to the CoinGecko API
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,ethereum",
            "vs_currencies": "usd"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # USD static value
        usd_rate = 1.00

        # Extract exchange rates between BITCOIN and USD options[BRL and EUR]
        btc_usd_rate = usd_rate / data['bitcoin']['usd']

        # Extract exchange rates between ETHERIUM and USD options[BRL and EUR]
        eth_usd_rate = usd_rate / data['ethereum']['usd']

        return {
            "USD": '{:.8f}'.format(usd_rate),
            "BTC": '{:.8f}'.format(btc_usd_rate),
            "ETH": '{:.8f}'.format(eth_usd_rate)
        }
    except requests.RequestException as e:
        print(f"Error fetching CoinGecko values: {e}")
        return None


def get_open_exchange_rates_values():
    try:
        # Make a GET request to the Open Exchange Rates API
        url = "https://open.er-api.com/v6/latest/USD"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        brl_rate = data['rates']['BRL']
        eur_rate = data['rates']['EUR']

        return {
            "BRL": '{:.8f}'.format(brl_rate),
            "EUR": '{:.8f}'.format(eur_rate)
        }
    except requests.RequestException as e:
        print(f"Error fetching Open Exchange Rates values: {e}")
        return None


def get_currency_values():
    coingecko_values = get_coingecko_values()
    exchange_rates_values = get_open_exchange_rates_values()

    if coingecko_values is None or exchange_rates_values is None:
        return None

    return {**coingecko_values, **exchange_rates_values}

