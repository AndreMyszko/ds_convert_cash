from rest_framework.views import APIView
from rest_framework.response import Response
from core.services.currency_service import get_currency_values
from core.services.exchange_service import convert_currency


class CurrencyValuesView(APIView):
    def get(self, request):
        currency_values = get_currency_values()
        if currency_values is None:
            return Response({"error": "Failed to fetch currency values."}, status=500)
        return Response({"currency": currency_values})


class CurrencyExchangeView(APIView):
    def get(self, request):
        # Get query parameters from the request
        from_currency = request.query_params.get('from')
        to_currency = request.query_params.get('to')
        amount = float(request.query_params.get('amount'))

        # Fetch the exchange rates
        currency_values = get_currency_values()
        if currency_values is None:
            return Response({"error": "Failed to fetch currency values."}, status=500)

        # Perform the currency conversion
        converted_amount = convert_currency(
            amount, from_currency, to_currency, currency_values)
        if converted_amount is None:
            return Response({"error": "Failed to convert currency."}, status=500)

        # Return the exchange result in the response
        return Response({
            "exchange": {
                "from": from_currency,
                "amount": '{:.8f}'.format(amount),
                "to": to_currency,
                "exchange": converted_amount
            }
        })

