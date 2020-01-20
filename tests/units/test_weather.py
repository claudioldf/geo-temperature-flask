import unittest
import os

from src.utils.weather_service import WeatherService

class TestWeatherService(unittest.TestCase):

    def setUp(self):
        # Values for sample data propose
        self.sample_zipcode = "94040"
        self.sample_country_code = "us"
        self.sample_api_key = os.getenv("OPEN_WEATHER_MAP_KEY")

        self.weather_service = WeatherService(self.sample_api_key)


    # Test constants values
    def test_units_constants(self):
        self.assertEqual("metric", WeatherService.UNIT_METRIC)
        self.assertEqual("imperial", WeatherService.UNIT_IMPERIAL)


    # Test private methods
    def test__get_base_endpoint(self):
        expected_endpoint = "https://api.openweathermap.org/data/2.5" 
        self.assertEqual(expected_endpoint, self.weather_service._get_base_endpoint())

    def test__get_endpoint_by_zipcode(self):
        zipcode = "10013"
        country_code = "us"

        expected_endpoint = "https://api.openweathermap.org/data/2.5/weather?appid={appid}&units={units}&zip={zipcode},{country_code}".format(
            appid=self.sample_api_key,
            units="imperial",
            zipcode=zipcode,
            country_code=country_code
        )

        self.assertEqual(expected_endpoint, self.weather_service._get_endpoint_by_zipcode(zipcode, country_code))


    # Test public methods
    def test_fetch_current_temperature_by_zipcode_with_a_valid_zipcode_and_country_code(self):
        temperature = self.weather_service.fetch_current_temperature_by_zipcode(self.sample_zipcode, self.sample_country_code)

        self.assertEqual("ok", temperature["status"])
        self.assertEqual(True, "status" in temperature)
        self.assertEqual(True, "time" in temperature)
        self.assertEqual(True, "current" in temperature)
        self.assertEqual(True, "min" in temperature)
        self.assertEqual(True, "max" in temperature)
        self.assertEqual(True, "symbol" in temperature)
        self.assertEqual(True, "condition" in temperature)

    def test_fetch_current_temperature_by_zipcode_with_an_invalid_zipcode(self):
        temperature = self.weather_service.fetch_current_temperature_by_zipcode("0000000", self.sample_country_code)

        self.assertEqual("error", temperature["status"])
        self.assertEqual("There is no weather information available for this address.", temperature["error_message"])

    def test_fetch_current_temperature_by_zipcode_with_invalid_country_code(self):
        temperature = self.weather_service.fetch_current_temperature_by_zipcode(self.sample_zipcode, "invalid")

        self.assertEqual("error", temperature["status"])
        self.assertEqual("There is no weather information available for this address.", temperature["error_message"])

    def test_temperature_symbol(self):
        weather_service_c = WeatherService(self.sample_api_key, WeatherService.UNIT_METRIC)
        self.assertEqual("ºC", weather_service_c.temperature_symbol())

        weather_service_f = WeatherService(self.sample_api_key, WeatherService.UNIT_IMPERIAL)
        self.assertEqual("ºF", weather_service_f.temperature_symbol())
