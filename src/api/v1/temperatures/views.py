import json, jsons, os
from datetime import datetime

from flask import Response, request
from cerberus import Validator

from src import db, app
from src.api.v1.temperatures.models import Temperature
from src.utils.weather_service import WeatherService

class TemperatureView:
    @app.route('/api/v1/temperatures/search', methods=['GET'])
    def search():
        zipcode = request.args.get("zipcode")
        country_code = request.args.get("country_code")

        try:
            if(zipcode == ""):
                raise ValueError("zipcode argument is required on query string")

            if(country_code == ""):
                raise ValueError("country_code argument is required on query string")

            
            temperature = Temperature.query.find_last_by_location_within_1hour(zipcode, country_code)
            if temperature != None:
                response_json = {
                    "status": "ok",
                    "zipcode": temperature.zipcode,
                    "country": temperature.country_code,
                    "weather": {
                        "current": str(int(round(float(temperature.temperature)))),
                        "unit": temperature.unit
                    } 
                }
            else:
                # Get weather info
                weather_service = WeatherService(os.getenv("OPEN_WEATHER_MAP_KEY"), WeatherService.UNIT_IMPERIAL)
                weather_infos = weather_service.fetch_current_temperature_by_zipcode(zipcode, country_code)

                if(weather_infos["status"] != "ok"):
                    raise ValueError(weather_infos["error_message"])

                response_json = {
                    "status": "ok",
                    "zipcode": zipcode,
                    "country": country_code,
                    "weather": {
                        "current": weather_infos["current"],
                        "unit": weather_infos["symbol"]
                    }
                }

            return Response(json.dumps(response_json), content_type='application/json')

        except(ValueError) as e:
            response = {}
            response["status"] = "error"
            response["error_message"] = e.args[0]
            return Response(json.dumps(response), content_type='application/json')

    @app.route('/api/v1/temperatures', methods=['GET'])
    def index():
        zipcode = request.args.get("zipcode")
        temperatures = Temperature.query.get_all_by_zipcode(zipcode)

        return Response(json.dumps([d.to_json_object() for d in temperatures]), content_type='application/json')

    @app.route('/api/v1/temperatures', methods=['POST'])
    def create():
        now = datetime.utcnow()

        document = {
            'date': now.date(),
            'time': now.strftime("%H:%M:%S"),
            'zipcode': request.json.get("zipcode"),
            'country_code': request.json.get("country_code"),
            'city_name': request.json.get("city_name"),
            'district': request.json.get("district"),
            'address': request.json.get("address"),
            'temperature': request.json.get("temperature"),
            'unit': request.json.get("unit")
        }

        temperature = Temperature(document)
        validator = Validator( Temperature.validation_schema() )

        try:            
            if (validator.validate(document) == False):
                raise ValueError('Invalid parameters on request payload')
            
            db.session.add(temperature)
            db.session.commit()
            db.session.flush()

            http_status_code = 201
        except: 
            http_status_code = 422
            return Response(json.dumps({ 
                'status': 'error', 
                'validations': validator.errors
            }), content_type='application/json', status=http_status_code)

        return Response(jsons.dumps(temperature.to_json_object()), content_type='application/json', status=http_status_code)