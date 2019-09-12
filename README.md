[![Build Status](https://travis-ci.org/arthuroe/flight_booking_api.svg?branch=develop)](https://travis-ci.org/arthuroe/flight_booking_api)
[![Coverage Status](https://coveralls.io/repos/github/arthuroe/flight_booking_api/badge.svg?branch=develop)](https://coveralls.io/github/arthuroe/flight_booking_api?branch=develop)

### Flight Booking API

This application enables a user to check and book available flights.

#### Features

- A user can login and register.
- A user can view all available flights.
- A user can book a flight.
- A user gets notified after booking a flight.
- A user gets a reminder before the flight.
- An admin can add flights.
- An admin can view how many people have made reservations for a particular flight in a day.

#### Development setup

- Clone this repo and navigate into the project's directory

  - `$ git clone https://github.com/arthuroe/flight_booking_api && cd flight_booking_api`

- Create a python3 virtual environment for the project and activate it.

  - To install the virtual environment wrapper `mkvirtualenv` you can follow [this](https://jamie.curle.io/installing-pip-virtualenv-and-virtualenvwrapper-on-os-x).
  - `$ mkvirtualenv --py=python3 flight_booking_api`

- Setup postgresql database

  - `$ create a database`
  - `$ create user`

- Run Migrations for the database

  - `$ python manage.py db init`
  - `$ python manage.py db migrate`
  - `$ python manage.py db upgrade`

- Install the project's requirements

  - `$ pip install requiremenst.txt`

- Copy `.env.sample` into `.env` in the flight_booking_api which is the base folder of the project. You should adjust it according to your own local settings.

- Setup Redis

  - `$ brew install redis`
  - `$ run redis-server`

- Install Celery. For more information on installing Celery for Flask Applications [this](http://flask.pocoo.org/docs/0.12/patterns/celery/).

  - `$ pip install celery`

- To start Celery worker and beat

  - `$ celery worker -A app.celery --loglevel=INFO`
  - `$ celery beat -A app.celery --schedule=/tmp/celerybeat-schedule --loglevel=INFO --pidfile=/tmp/celerybeat.pid`

- Export the environment variables in the .env

  - `$ export $(cat .env)`

- Run tests on the code in the project folder with

  - `$ pytest`

- Run the application
  - `$ python run.py`
