from rest_framework.views import APIView
from rest_framework.response import Response
import requests


class CurrencyValuesView(APIView):
    def get(self, request):

        # Make a GET request to the CoinGecko API
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,ethereum",
            "vs_currencies": "usd,brl,eur"
        }
        response = requests.get(url, params=params)
        data = response.json()

        # USD static value
        usd_rate = 1.00

        # Extract exchange rates between BITCOIN and USD options[BRL and EUR]
        # btc_brl_rate = data['bitcoin']['brl']
        # btc_eur_rate = data['bitcoin']['eur']
        btc_usd_rate = usd_rate / data['bitcoin']['usd']

        # Extract exchange rates between ETHERIUM and USD options[BRL and EUR]
        # eth_brl_rate = data['ethereum']['brl']
        # eth_eur_rate = data['ethereum']['eur']
        eth_usd_rate = usd_rate / data['ethereum']['usd']

        # Make a GET request to the Open Exchange Rates API
        url = "https://open.er-api.com/v6/latest/USD"
        response = requests.get(url)
        data = response.json()

        # usd_rate = data['rates']['USD']
        brl_rate = data['rates']['BRL']
        eur_rate = data['rates']['EUR']

        # Return the exchange rates in the response
        return Response({
            "currency": {
                "USD": '{:.8f}'.format(usd_rate),
                "BRL": '{:.8f}'.format(brl_rate),
                "EUR": '{:.8f}'.format(eur_rate),
                "BTC": '{:.8f}'.format(btc_usd_rate),
                "ETH": '{:.8f}'.format(eth_usd_rate)
            }
        })


class CurrencyExchangeView(APIView):
    def get(self, request):
        # Get query parameters from the request
        from_currency = request.query_params.get('from')
        to_currency = request.query_params.get('to')
        amount = float(request.query_params.get('amount'))

        # Fetch the exchange rates from the CurrencyValuesView
        response = CurrencyValuesView().get(request)
        exchange_rates = response.data['currency']

        # Perform the currency conversion
        if from_currency == 'USD':
            converted_amount = amount * float(exchange_rates[to_currency])
        elif to_currency == 'USD':
            converted_amount = amount / float(exchange_rates[from_currency])
        else:
            converted_amount = amount * (float(exchange_rates[to_currency]) / float(exchange_rates[from_currency]))

        # Return the exchange result in the response
        return Response({
            "exchange": {
                "from": from_currency,
                "amount": str('{: .8f}'.format(amount)),
                "to": to_currency,
                "exchange": str('{:.8f}'.format(converted_amount))
            }
        })
