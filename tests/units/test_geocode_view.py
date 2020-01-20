import json
import os

from src import app

import requests
import requests_mock
import unittest
# from unittest.mock import patch, Mock

class TemperatureView(unittest.TestCase):
    def setUp(self):
        # Sample data's
        self.sample_zipcode = '94040'
        self.sample_country_code = 'us'
        self.sample_address = 'Franklin St New York, NY'

        self.client = app.test_client()

    # GET /api/v1/temperatures/searchByAddress
    def test_search_by_address_with_valid_address(self):
        response = self.client.get('http://127.0.0.1:5000/api/v1/geocode/searchByAddress?q='+self.sample_address)
        self.assertEqual(200, response.status_code)
        self.assertIn('application/json', response.content_type)
        self.assertEqual("Franklin St", response.json["address"])
        self.assertEqual("New York", response.json["city_name"])
        self.assertEqual("NY", response.json["district"])
        self.assertEqual("US", response.json["country_code"])
        self.assertEqual("10013", response.json["zipcode"])
        self.assertEqual("ok", response.json.get("status"))

    # GET /api/v1/temperatures/searchByAddress
    def test_search_by_address_with_invalid_address(self):
        response = self.client.get('http://127.0.0.1:5000/api/v1/geocode/searchByAddress?q=testinvalidaddress')
        self.assertEqual(200, response.status_code)
        self.assertIn('application/json', response.content_type)
        self.assertEqual(True, "error_message" in response.json)
        self.assertEqual("error", response.json.get("status"))