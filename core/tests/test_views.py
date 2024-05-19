from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch
from core.services.exchange_service import convert_currency



class TestCurrencyViews(TestCase):

    def setUp(self):
        self.client = APIClient()

    @patch('core.services.exchange_service.convert_currency')
    def test_currency_values_view(self, mock_get_currency_values):
        mock_get_currency_values.return_value = {
            "USD": "1.00000000",
            "BRL": "5.12957200",
            "EUR": "0.91971600",
            "BTC": "0.00002000",
            "ETH": "0.00025000"
        }

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['currency']['USD'], '1.00000000')

    @patch('core.services.exchange_service.convert_currency')
    def test_currency_exchange_view(self, mock_get_currency_values):
        mock_get_currency_values.return_value = {
            "USD": "1.00000000",
            "BRL": "5.12957200",
            "EUR": "0.91971600",
            "BTC": "0.00002000",
            "ETH": "0.00025000"
        }

        response = self.client.get('/exchange/', {'from': 'USD', 'to': 'BRL', 'amount': 10})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['exchange']['exchange'], '51.29572000')

