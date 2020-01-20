# About

This documentation is part of the development of the backend application, which is responsible for support the required information of Weather frontend application.

The backend application was developed using Python 3.7 + Flask framework, in order to support the requirements of this proposed challenge.

And he frontend application was built using React library.

This repository contains only the backend application project.
In order to run the frontend application check this repository:
https://github.com/claudioldf/geo-temperature-react

# How to setup and runs backend application
### Database steps:
This project use MySQL database, you could try to use other database driver, however I had just test it on MySQL, but Flask framework support others database drivers like PostgreSQL. In this case you can check the ".env-sample" file to change the connection string.

If you use docker, on the file docker-compose.yml, there is already a container to run a instance of mysql + flask application.
So in this case, you don't need to setup any database by yourself. You just have to copy the file .env-sample to .env and turn the docker containers up ("docker-compose up -d db_backend_flask").

If you don't use docker, you will need to setup MySQL before, create a new database and after that setup your username, password, host, port and database name on .env file (there is some examples on .env-sample)


### Application steps:
#### With Docker + docker-compose (Recommended):
```bash
# 1. Copy .env-sample file to .env.
$ cp .env-sample .env
# NOTE: You must check this file .env and change the database connection string to yours.

# 2. Turn the container up. Note that the first time you run, it will download and build the container image.
$ docker-compose up -d
# The application will be availiable at url: http://localhost:5000

# 3. Run the db migrations scripts:
$ docker-compose run app_backend_flask flask db upgrade

# 4. If you want to run the units tests:
$ docker-compose run app_backend_flask py.test
```

#### Without Docker:
```bash
# On bash/terminal run:

# 1. Install virtualenv
$ pip3 install virtualenv

# 2. Create you virtualenv
$ virtualenv -p python3 env

# 3. Active the virtualenv
$ source env/bin/activate

# 4. Install the required python libs
$ pip3 install -r requirements.txt

# 5. Copy .env-sample file to .env
$ cp .env-sample .env

# 6. Edit the .env file and change this environment variables:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://myUsername:myPassword@myHost/myDatabaseName?charset=utf8mb4"

    OPEN_WEATHER_MAP_KEY = PUT_YOUR_OPEN_WEATHER_MAP_KEY

    GOOGLE_GEOCODE_KEY = PUT_YOUR_GOOGLE_GEOCODE_KEY

    # NOTE: I keep my keys on .env-sample to make it easy to test.

# 7. Run db migrations scripts:
$ flask db upgrade

# 7. Run unit tests
$ py.test 

# 8. Run the server
$ flask run
  # or #
$ python3 app.py
```

---

# Backend - API Documentation 

## Endpoints

#### Production
There is no production endpoint at the moment

#### Development
http://localhost:5000/api/v1/

---

## Methods - Geocode Module

> ### **GET /api/v1/geocode/searchByAddress**

    Obtain informations about a given address, such as zipcode, country code, city name, district and address.

#### **Params:**
- q (**required**) - Address to get this informations.  Example: Franklin St, New York, NY 

#### **Request Example:**
```bash
curl -H "Content-Type: application/json" -X GET "http://localhost:5000/api/v1/geocode/searchByAddress?q=Franklin%20St%20New%20York,%20NY"
```

#### **Response:**
- Example of success response
```json
{
  "status": "ok",
  "address": "Franklin St",
  "city_name": "New York",
  "district": "NY",
  "country_code": "US",
  "zipcode": "10013"
}
```
- Example of error response
```json
{
  "status": "error",
  "error_message": "The given address was not found on Google Geocode API. Please review it and try again"
}
```

---

> ### **GET /api/v1/temperatures/search**

    Obtain weather information about a given zip code and country code.
    
    Note: Everytime a request is comming, we firstly check on our database if someone has searched by the same zipcode and country code within 1 hour. 
    
    If found, then we return the cached information, otherwise we make a request to ​"Open Weather Map’s API" and then persist it on database.

#### **Params:**
- zipcode (**required**) The zipcode that you need to check the temperature. Example: 10013
- country_code (**required**) - The country code that you need to check the temperature. Example: "US" 

#### **Request Example:**
```bash
curl -H "Content-Type: application/json" -X GET "http://localhost:5000/api/v1/temperatures/search?zipcode=10013&country_code=us" 
```

#### **Response:**
- Example of success response
```json
{
  "status": "ok",
  "zipcode": "10013",
  "country": "US",
  "weather": {
    "current": 50.77,
    "unit": "ºF",
  }
}
```
- Example of error response
```json
{
  "status": "error",
  "error_message": "There is no weather information available for this address."
}
```

---

> ### **GET /api/v1/temperatures**

    List the log histories of all temperature already searched. Optionaly you could filter by country_code and zipcode throught query string parameters

#### **Filters params:**
- zipcode (**optional**)
- country_code (**optional**)

#### **Request Example:**
```bash
curl -H "Content-Type: application/json" -X GET "http://localhost:5000/api/v1/temperatures" 
```

#### **Response:**
- Example of response
```json
[
  {
    "id": 1,
    "date": "2019-10-19",
    "time": "20:03:31",
    "zipcode": 10013,
    "country_code": "US",
    "city_name": "New York",
    "district": "NY",
    "address": "Franklin St",
    "temperature": "63",
    "unit": "ºF"
  },
  ...
  {
    "id": 9,
    "date": "2019-10-20",
    "time": "02:18:55",
    "zipcode": 10013,
    "country_code": "US",
    "city_name": "New York",
    "district": "NY",
    "address": "Franklin St",
    "temperature": "50",
    "unit": "ºF"
  }
]
```

---

> ### **GET /api/v1/temperatures**

    Create a new temperature log on database

#### **Params:**
- zipcode - Integer value 
- country_code - String value with the country ISO code
- city_name - String value
- district - String value
- address - String value with the address searched
- temperature - Value in float format that represents the current temperature
- unit - Temperature unit (must be ºF or ºC)

#### **Request Payload Example:**
```json
{
	"zipcode": 10013,
	"country_code": "US",
	"city_name": "New York",
	"district": "NY",
	"address": "Franklin St",
	"temperature": 50.00,
	"unit": "ºF"
}
```

#### **Request Example:**
```bash
curl -H "Content-Type: application/json" -X POST -d '{"zipcode": 10013, "country_code": "US", "city_name": "New York", "district": "NY", "address": "Franklin St", "temperature": 50.00, "unit": "ºF"}' "http://localhost:5000/api/v1/temperatures"
```

#### **Response:**
- Example of response
```json
{
  "id": 1,
  "date": "2019-10-19",
  "time": "18:11:32",
  "zipcode": 10013,
  "country_code": "US",
  "city_name": "New York",
  "district": "NY",
  "address": "Franklin St",
  "temperature": "50",
  "unit": "ºF"
}
