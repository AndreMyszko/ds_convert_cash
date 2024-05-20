from django.test import TestCase
from unittest.mock import patch
from core.services.currency_service import (get_coingecko_values,
                                            get_open_exchange_rates_values)


class TestCurrencyServices(TestCase):

    @patch('core.services.currency_service.get_coingecko_values')
    def test_get_coingecko_values(self, mock_get):
        # mock was not used at the end of the day...
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

        # Check if BTC and ETH value is a string
        try:
            self.assertIsInstance(result['BTC'], str)
        except AssertionError:
            self.fail(f"Expected BTC to be a str, but got {
                      type(result['BTC'])}")
        try:
            self.assertIsInstance(result['ETH'], str)
        except AssertionError:
            self.fail(f"Expected ETH to be a str, but got {
                      type(result['ETH'])}")

        # Check if BTC and ETH value can be converted to a float
        try:
            btc_value = float(result['BTC'])
        except ValueError:
            self.fail("Returned BTC value is not a float")

        try:
            eth_value = float(result['ETH'])
        except ValueError:
            self.fail("Returned ETH value is not a float")

        # Check if BTC and ETH value is within an expected range (max/min value)
        try:
            self.assertTrue(0 < btc_value < 1)
        except AssertionError:
            self.fail(f"Expected BTC to be between 0 and 1, but got {
                      result['BTC']}")

        try:
            self.assertTrue(0 < eth_value < 1)
        except AssertionError:
            self.fail(f"Expected ETH to be between 0 and 1, but got {
                      result['ETH']}")

    @patch('core.services.currency_service.get_open_exchange_rates_values')
    def test_get_open_exchange_rates_values(self, mock_get):
        # mock was not used at the end of the day...
        mock_response = {
            "rates": {
                "BRL": 5.129572,
                "EUR": 0.919716
            }
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_open_exchange_rates_values()

        # Check if BRL and EUR value is a string
        try:
            self.assertIsInstance(result['BRL'], str)
        except AssertionError:
            self.fail(f"Expected BRL to be a str, but got {
                      type(result['BRL'])}")

        try:
            self.assertIsInstance(result['EUR'], str)
        except AssertionError:
            self.fail(f"Expected EUR to be a str, but got {
                      type(result['EUR'])}")

        # Check if BRL and EUR value can be converted to a float
        try:
            brl_value = float(result['BRL'])
        except ValueError:
            self.fail("Returned BRL value is not a float")

        try:
            eur_value = float(result['EUR'])
        except ValueError:
            self.fail("Returned EUR value is not a float")

        # Only positive values for test purpose (min value)
        try:
            self.assertGreater(brl_value, 0)
        except AssertionError:
            self.fail(f"Expected BRL to be greater than 0, but got {
                      result['BRL']}")

        try:
            self.assertGreater(eur_value, 0)
        except AssertionError:
            self.fail(f"Expected EUR to be greater than 0, but got {
                      result['EUR']}")

        # Set a reasonable upper bound (max value)
        try:
            self.assertLess(brl_value, 10)
        except AssertionError:
            self.fail(f"Expected BRL to be less than 10, but got {
                      result['BRL']}")

        try:
            self.assertLess(eur_value, 2)
        except AssertionError:
            self.fail(f"Expected EUR to be less than 2, but got {
                      result['EUR']}")
