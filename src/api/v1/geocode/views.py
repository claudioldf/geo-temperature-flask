import json, os, re
from flask import Response, request
from src import db, app
from src.api.v1.temperatures.models import Temperature
from src.utils.weather_service import WeatherService

import googlemaps
import geocoder

class GeocodeView:

    @app.route('/api/v1/geocode/searchByAddress', methods=['GET'])
    def searchByAddress():
        address = request.args.get("q")

        response = {
            "status": "ok",
        }

        try:
            if(os.getenv("GOOGLE_GEOCODE_KEY") == None):
                raise Exception("The Google Geocode API Key was not given.")

            gmaps = googlemaps.Client(key=os.getenv("GOOGLE_GEOCODE_KEY"))
            response_gmaps = gmaps.geocode(address)

            if(len(response_gmaps) == 0):
                raise Exception("The given address was not found on Google Geocode API. Please review it and try again")
            
        except(googlemaps.exceptions.ApiError, Exception) as e:
            response["status"] = "error"
            response["error_message"] = e.args[0]
            return Response(json.dumps(response), content_type='application/json')


        address_details = response_gmaps[0]["address_components"]
        for info in address_details:
            if ("route" in info["types"]):
                response["address"] = info["short_name"]
            if ("locality" in info["types"]):
                response["city_name"] = info["short_name"]
            if ("administrative_area_level_1" in info["types"]):
                response["district"] = info["short_name"]
            if ("country" in info["types"]):
                response["country_code"] = info["short_name"]
            if ("postal_code" in info["types"]):
                response["zipcode"] = re.sub(r'\D+', '', info["short_name"]) # Regex replace to keep only digits

        return Response(json.dumps(response), content_type='application/json')
