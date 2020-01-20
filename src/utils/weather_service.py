import requests

class WeatherService:
    _api_base_url = "https://api.openweathermap.org/data"
    _api_key = None
    _api_version = None
    _units = None
  
    UNIT_METRIC = "metric"
    UNIT_IMPERIAL = "imperial"

    def __init__(self, api_key, units = UNIT_IMPERIAL, api_version = 2.5):
        self._api_key = api_key
        self._api_version = api_version
        self._units = units

    def fetch_current_temperature_by_zipcode(self, zipcode, country_code):
        try:
            endpoint = self._get_endpoint_by_zipcode(zipcode, country_code)
            data = requests.get(endpoint).json()

            if (int(data["cod"]) == 404):
                raise ValueError("There is no weather information available for this address.")

            if (int(data["cod"]) == 401):
                raise ValueError("Then given Open Weather API Key is invalid or expired.")

            if (int(data["cod"]) == 500):
                raise ValueError("The Open Weather API is not available at this moment. Please, try again within some minutes.")

            if (int(data["cod"]) != 200):
                raise ValueError("Something unexpected happened. The Open Weather API returned the following status code: {cod}".format(cod=data['cod']))

            response = {}
            response["status"] = "ok"
            response["time"] = data["dt"]
            response["current"] = data["main"]["temp"]
            response["min"] = data["main"]["temp_min"]
            response["max"] = data["main"]["temp_max"]
            response["symbol"] = self.temperature_symbol()
            response["condition"] = data["weather"][0]["main"]
        except(ValueError)  as e:
            response = {}
            response["status"] = "error"
            response["error_message"] = e.args[0]

        return response

    def temperature_symbol(self):
        return {
            self.UNIT_METRIC: 'ºC',
            self.UNIT_IMPERIAL: 'ºF',
        }[self._units]
        
    def _get_base_endpoint(self):
        return "{base_url}/{version}".format(
            base_url=self._api_base_url, 
            version=self._api_version
        )

    def _get_endpoint_by_zipcode(self, zipcode, country_code):
        return "{base_url}/{version}/weather?appid={appid}&units={units}&zip={zipcode},{country_code}".format(
            base_url=self._api_base_url, 
            version=self._api_version,
            appid=self._api_key,
            units=self._units,
            zipcode=zipcode,
            country_code=country_code
        )

    
