from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from app.auth import token_required
from app.models import Flight
from .helpers import get_available_flights


class FlightsView(MethodView):

    @token_required
    def get(self, *args, **kwargs):
        flights = Flight.fetch_all()
        if get_available_flights():
            flights = [flight.serialize_items()
                       for flight in get_available_flights()]
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
