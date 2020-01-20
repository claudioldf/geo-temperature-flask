import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# Initialize app from Flask class
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Setup SQLAlchemy
# See: https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/

# Database connections
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI') # Sqlite

# Enable query debug. 
# NOTE: Should only be use on development/debug environment
app.config['SQLALCHEMY_RECORD_QUERIES'] = True 

# Initialize SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()

migrate = Migrate(app, db)

# Import views/routes
from src.api.v1.temperatures.views import TemperatureView
from src.api.v1.geocode.views import GeocodeView