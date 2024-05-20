from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch
from core.services.exchange_service import convert_currency



class TestCurrencyViews(TestCase):

    def setUp(self):
        self.client = APIClient()

    @patch('core.services.exchange_service.convert_currency')
    def test_currency_values_view(self, mock_get_currency_values):
        # mock was not used at the end of the day...
        mock_get_currency_values.return_value = {
            "USD": "1.00000000",
            "BRL": "5.12957200",
            "EUR": "0.91971600",
            "BTC": "0.00002000",
            "ETH": "0.00025000"
        }

        result = self.client.get('/')
        try:
            self.assertEqual(result.status_code, 200)
        except AssertionError:
            self.fail(f"Expected status code 200, but got {
                      result.status_code}")

        try:
            self.assertEqual(result.data['currency']['USD'], '1.00000000')
        except AssertionError:
            self.fail(f"Expected USD to be '1.00000000', but got {
                      result.data['currency']['USD']}")

        # Check if BRL, EUR, BTC and ETH value is a string
        try:
            self.assertIsInstance(result.data['currency']['BRL'], str)
        except AssertionError:
            self.fail(f"Expected BRL to be a str, but got {
                      type(result.data['currency']['BRL'])}")

        try:
            self.assertIsInstance(result.data['currency']['EUR'], str)
        except AssertionError:
            self.fail(f"Expected EUR to be a str, but got {
                      type(result.data['currency']['EUR'])}")

        try:
            self.assertIsInstance(result.data['currency']['BTC'], str)
        except AssertionError:
            self.fail(f"Expected BTC to be a str, but got {
                      type(result.data['currency']['BTC'])}")

        try:
            self.assertIsInstance(result.data['currency']['ETH'], str)
        except AssertionError:
            self.fail(f"Expected ETH to be a str, but got {
                      type(result.data['currency']['ETH'])}")

        # Check if BRL, EUR, BTC and ETH value can be converted to a float
        try:
            brl_value = float(result.data['currency']['BRL'])
        except ValueError:
            self.fail("Returned BRL value is not a float")

        try:
            eur_value = float(result.data['currency']['EUR'])
        except ValueError:
            self.fail("Returned EUR value is not a float")

        try:
            btc_value = float(result.data['currency']['BTC'])
        except ValueError:
            self.fail("Returned BTC value is not a float")

        try:
            eth_value = float(result.data['currency']['ETH'])
        except ValueError:
            self.fail("Returned ETH value is not a float")

        # Check if BRL, EUR, BTC and ETH value is within an expected range (max/min value)
        try:
            self.assertGreater(brl_value, 0)
        except AssertionError:
            self.fail(f"Expected BRL to be greater than 0, but got {
                      result.data['currency']['BRL']}")

        try:
            self.assertGreater(eur_value, 0)
        except AssertionError:
            self.fail(f"Expected EUR to be greater than 0, but got {
                      result.data['currency']['EUR']}")

        try:
            self.assertLess(brl_value, 10)
        except AssertionError:
            self.fail(f"Expected BRL to be less than 10, but got {
                      result.data['currency']['BRL']}")

        try:
            self.assertLess(eur_value, 2)
        except AssertionError:
            self.fail(f"Expected EUR to be less than 2, but got {
                      result.data['currency']['EUR']}")

        try:
            self.assertTrue(0 < btc_value < 1)
        except AssertionError:
            self.fail(f"Expected BTC to be between 0 and 1, but got {
                      result.data['currency']['BTC']}")

        try:
            self.assertTrue(0 < eth_value < 1)
        except AssertionError:
            self.fail(f"Expected ETH to be between 0 and 1, but got {
                      result.data['currency']['ETH']}")
            

    @patch('core.services.exchange_service.convert_currency')
    def test_currency_exchange_view(self, mock_get_currency_values):
        # mock was not used at the end of the day...
        mock_get_currency_values.return_value = {
            "USD": "1.00000000",
            "BRL": "5.12957200",
            "EUR": "0.91971600",
            "BTC": "0.00002000",
            "ETH": "0.00025000"
        }

        result = self.client.get(
            '/exchange/', {'from': 'USD', 'to': 'BRL', 'amount': 10})
        self.assertEqual(result.data['exchange']['exchange'], '51.29572000')

        # Check response status code
        try:
            self.assertEqual(result.status_code, 200)
        except AssertionError:
            self.fail(f"Expected status code 200, but got {
                      result.status_code}")
            
        # Check if the exchange value is a string
        try:
            self.assertIsInstance(result.data['exchange']['exchange'], str)
        except AssertionError:
            self.fail(f"Expected exchange value to be a str, but got {
                      type(result.data['exchange']['exchange'])}")

        # Ensure the exchange value can be converted to a float
        try:
            exchange_value = float(result.data['exchange']['exchange'])
        except ValueError:
            self.fail("Returned exchange value is not a float")

        # Check if the exchange value is within an expected range (example range: 50 to 60)
        try:
            self.assertGreater(exchange_value, 40)
        except AssertionError:
            self.fail(f"Expected exchange value to be greater than 50, but got {
                      result.data['exchange']['exchange']}")

        try:
            self.assertLess(exchange_value, 80)
        except AssertionError:
            self.fail(f"Expected exchange value to be less than 60, but got {
                      result.data['exchange']['exchange']}")
            
