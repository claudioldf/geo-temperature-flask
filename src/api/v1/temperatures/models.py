from datetime import datetime, timedelta
from dataclasses import dataclass
from flask_sqlalchemy import BaseQuery
from sqlalchemy.sql import functions
from sqlalchemy import desc, text
from src import db
import json

class TemperatureQuery(BaseQuery):
    def get_all_by_zipcode(self, zipcode = "", country_code = ""):
        query = self

        if(country_code):
            query = query.filter_by(country_code = country_code)

        if(zipcode):
            query = query.filter_by(zipcode = zipcode)

        return query.all()

    def find_last_by_location_within_1hour(self, zipcode, country_code):
        sub_time = datetime.utcnow() + timedelta(hours=1, minutes=0)

        query = self
        
        query = query.filter(functions.concat(Temperature.date, ' ', Temperature.time).__ge__('2019-12-03 22:33:00'))

        if(country_code):
            query = query.filter_by(country_code = country_code)

        if(zipcode):
            query = query.filter_by(zipcode = zipcode)

        return query.order_by(text('date desc')).order_by(text('time desc')).limit(1).first()

@dataclass
class Temperature(db.Model):
    __tablename__ = 'temperatures'
    query_class = TemperatureQuery

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    zipcode = db.Column(db.Integer)
    country_code = db.Column(db.String(3))
    district = db.Column(db.String(60))
    city_name = db.Column(db.String(60))
    address = db.Column(db.String(60))
    temperature = db.Column(db.Float(asdecimal=True))
    unit = db.Column(db.String(2))

    def __init__(self, document):
        self.from_json_object(document)

    def to_json_object(self):
        return {
            'id': self.id,
            'date': str(self.date),
            'time': str(self.time),
            'zipcode': self.zipcode,
            'country_code': self.country_code,
            'city_name': self.city_name,
            'district': self.district,
            'address': self.address,
            'temperature': str(int(round(float(self.temperature)))),
            'unit': self.unit
        }

    def from_json_object(self, document):
        for key, value in document.items():
            setattr(self, key, value)

    @staticmethod
    def validation_schema():
        return {
            'date': {'type': 'date', 'required': True},
            'time': {'type': 'string', 'required': True},
            'zipcode': {'type': 'integer', 'required': True},
            'country_code': {'type': 'string', 'required': True, 'min': 2, 'max': 3},
            'city_name': {'type': 'string', 'required': True, 'max': 60},
            'district': {'type': 'string', 'required': True, 'max': 60},
            'address': {'type': 'string', 'required': True, 'max': 60},
            'temperature': {'type': 'float', 'required': True},
            'unit': {'type': 'string', 'required': True, 'max': 2},
        }    