import logging

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from app.auth import token_required, admin_required
from app.flights.helpers import get_available_flights
from app.models import Flight, db


class FlightsView(MethodView):

    @token_required
    def get(self, *args, **kwargs):
        flights = get_available_flights()
        if flights:
            flights = [flight.serialize()
                       for flight in flights]
            response = {
                'status': 'success',
                'flights': flights
            }
        else:
            response = {
                'status': 'success',
                'message': 'No available flights at the moment'
            }
        return make_response(jsonify(response)), 200

    @token_required
    @admin_required
    def post(self, *args, **kwargs):
        kwargs = request.json
        if not all(
                [kwargs.get('flight_name'), kwargs.get(
                    'flight_destination'), kwargs.get('flight_date')]
        ):
            response = {
                'status': 'fail',
                'message': ('Incomplete data. All fields are required')
            }
            return make_response(jsonify(response)), 400

        try:
            flight = Flight(**kwargs)
            flight.save()

            response = {
                'status': 'success',
                'message': 'Successfully added flight.'
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'Failed to add flight.'
            }
            return make_response(jsonify(response)), 400
