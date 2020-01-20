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

        self.client = app.test_client()

    # GET /api/v1/temperatures/search
    def test_search_valid_zipcode(self):
        response = self.client.get('http://127.0.0.1:5000/api/v1/temperatures/search?zipcode='+self.sample_zipcode+'&country_code'+self.sample_country_code)
        self.assertEqual(200, response.status_code)
        self.assertIn('application/json', response.content_type)

    def test_search_invalid_zipcode(self):
        response = self.client.get('http://127.0.0.1:5000/api/v1/temperatures/search?zipcode=0&country_code'+self.sample_country_code)
        self.assertEqual(200, response.status_code)
        self.assertEqual("error", response.json.get("status"))
        self.assertEqual(True, "error_message" in response.json)
        self.assertIn('application/json', response.content_type)

    # GET /api/v1/temperatures
    def test_home(self):
        response = self.client.get('http://127.0.0.1:5000/api/v1/temperatures')
        self.assertEqual(200, response.status_code)
        self.assertIn('application/json', response.content_type)

    # POST /api/v1/temperatures
    def test_create_valid_object(self):
        document = {"zipcode": 10013, "country_code": "US", "city_name": "New York", "district": "NY", "address": "Franklin St", "temperature": 50, "unit": "ºF"}

        response = self.client.post('http://127.0.0.1:5000/api/v1/temperatures', json=document)
        self.assertEqual(201, response.status_code)
        self.assertIn('application/json', response.content_type)
        self.assertEqual(True, "id" in response.json)
        self.assertEqual(document["zipcode"], response.json["zipcode"])
        self.assertEqual(document["country_code"], response.json["country_code"])
        self.assertEqual(document["city_name"], response.json["city_name"])
        self.assertEqual(document["district"], response.json["district"])
        self.assertEqual(document["address"], response.json["address"])
        self.assertEqual(str(round(document["temperature"])), response.json["temperature"])
        self.assertEqual(document["unit"], response.json["unit"])
        self.assertEqual(False, "validations" in response.json)

    def test_create_invalid_object(self):
        response = self.client.post('http://127.0.0.1:5000/api/v1/temperatures', json={"zipcode": "", "country_code": "", "city_name": "", "district": "", "address": "", "temperature": "", "unit": ""})
        self.assertEqual(422, response.status_code)
        self.assertIn('application/json', response.content_type)
        self.assertEqual(True, "status" in response.json)
        self.assertEqual(True, "validations" in response.json)
        self.assertEqual("error", response.json.get("status"))