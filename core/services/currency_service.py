import requests


def get_coingecko_values():
    try:
        # Make a GET request to the CoinGecko API
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,ethereum,litecoin,ripple,bitcoin-cash,cardano,"
                   "polkadot,stellar,chainlink,binancecoin,tether,dogecoin,"
                   "solana,uniswap,vechain,monero,eos,aave,cosmos,tron,"
                   "tezos,iota,neo,dash,zcash",
            "vs_currencies": "usd"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # USD static value
        usd_rate = 1.00

        # Dictionary to map cryptocurrency IDs to their symbols
        crypto_symbols = {
            'bitcoin': 'BTC', 
            'ethereum': 'ETH', 
            'litecoin': 'LTC', 
            'ripple': 'XRP',
            'bitcoin-cash': 'BCH', 
            'cardano': 'ADA', 
            'polkadot': 'DOT', 
            'stellar': 'XLM',
            'chainlink': 'LINK', 
            'binancecoin': 'BNB', 
            'tether': 'USDT', 
            'dogecoin': 'DOGE',
            'solana': 'SOL', 
            'uniswap': 'UNI', 
            'vechain': 'VET', 
            'monero': 'XMR', 
            'eos': 'EOS',
            'aave': 'AAVE', 
            'cosmos': 'ATOM', 
            'tron': 'TRX', 
            'tezos': 'XTZ', 
            'iota': 'MIOTA',
            'neo': 'NEO', 
            'dash': 'DASH', 
            'zcash': 'ZEC'
        }

        # Initialize dictionary to store exchange rates
        exchange_rates = {"USD": '{:.8f}'.format(usd_rate)}

        # Iterate through the crypto_symbols dictionary and extract their rates
        for crypto_id, symbol in crypto_symbols.items():
            try:
                rate = usd_rate / data[crypto_id]['usd']
                exchange_rates[symbol] = '{:.8f}'.format(rate)
            except KeyError:
                print(f"Error: No rate found for {crypto_id}")

        return exchange_rates
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

        # Extract rates for desired currencies
        currencies = ['BRL', 'EUR', 'GBP', 'JPY',
                      'AUD', 'CAD', 'CHF', 'CNY', 'SEK', 'NZD']
        exchange_rates = {currency: '{:.8f}'.format(
            data['rates'][currency]) for currency in currencies}

        return exchange_rates

    except requests.RequestException as e:
        print(f"Error fetching Open Exchange Rates values: {e}")
        return None


def get_currency_values():
    coingecko_values = get_coingecko_values()
    exchange_rates_values = get_open_exchange_rates_values()

    if coingecko_values is None or exchange_rates_values is None:
        return None

    return {**coingecko_values, **exchange_rates_values}

