import logging

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from .helpers import get_available_flights
from app.auth import token_required
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

    def post(self, *args, **kwargs):
        post_data = request.json
        flight_name = post_data.get('name')
        flight_destination = post_data.get('destination')
        flight_date = post_data.get('date')
        flight_number = post_data.get('number')
        capacity = post_data.get('capacity')

        if not all([flight_name, flight_destination, flight_date]):
            response = {
                'status': 'fail',
                'message': ('Incomplete data. All fields are required')
            }
            return make_response(jsonify(response)), 400

        try:
            flight = Flight(
                flight_number=flight_number, flight_name=flight_name,
                flight_destination=flight_destination, flight_date=flight_date,
                capacity=capacity
            )
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
