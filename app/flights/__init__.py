from flask import Blueprint

from app.flights.views import FlightsView

flight_blueprint = Blueprint('flight', __name__, url_prefix='/api/v1')
flights_view = FlightsView.as_view('flights_api')
flight_blueprint.add_url_rule(
    '/flights',
    view_func=flights_view,
    methods=['GET']
)
