from django.test import TestCase
from unittest.mock import patch
from core.services.currency_service import (get_coingecko_values, 
                                            get_open_exchange_rates_values, get_currency_values)


class TestCurrencyServices(TestCase):

    @patch('core.services.currency_service.get_coingecko_values')
    def test_get_coingecko_values(self, mock_get):
        mock_response = {
            "bitcoin": {
                "usd": 50000,
            },
            "ethereum": {
                "usd": 4000,
            }
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_coingecko_values()
        self.assertEqual(result['BTC'], '0.00002000')
        self.assertEqual(result['ETH'], '0.00025000')

    @patch('core.services.currency_service.get_open_exchange_rates_values')
    def test_get_open_exchange_rates_values(self, mock_get):
        mock_response = {
            "rates": {
                "BRL": 5.129572,
                "EUR": 0.919716
            }
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_open_exchange_rates_values()
        self.assertEqual(result['BRL'], '5.12957200')
        self.assertEqual(result['EUR'], '0.91971600')
