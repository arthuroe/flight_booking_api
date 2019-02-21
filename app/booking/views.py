import logging

from datetime import datetime
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from sqlalchemy import extract

from app.auth import token_required, admin_required
from app.flights import check_flight_is_available
from app.models import Booking, Flight
from app.notifications import send_email


class BookingView(MethodView):
    """
    View for booking a flight
    """
    decorators = [token_required]

    def post(self, current_user):
        post_data = request.json

        flight_id = post_data.get('flight_id')
        user_id = current_user.id

        if not flight_id:
            response = {
                'status': 'fail',
                'message': 'Incomplete data. All fields are required'
            }
            return make_response(jsonify(response)), 400

        flight = Flight.find_first(id=flight_id)

        if not flight:
            response = {
                'status': 'fail',
                'message': 'flight does not exist'
            }
            return make_response(jsonify(response)), 400

        if check_flight_is_available(flight):
            try:
                booking = Booking(flight_id=flight_id, user_id=user_id)
                booking.save()
                send_email('Booked Flight', [current_user.username],
                           'Booking', (
                    f'Hey {current_user.name},\n'
                    f'You have successfully booked {flight.flight_name}'
                    f' {flight.flight_number} '
                    f'scheduled for {flight.flight_date}')
                )
                response = {
                    'status': 'success',
                    'message': 'Successfully booked flight.'
                }
                return make_response(jsonify(response)), 201
            except Exception as e:
                logging.error(f"An error has occurred  {e}")
                response = {
                    'status': 'fail',
                    'message': 'Failed to book flight.'
                }
                return make_response(jsonify(response)), 400
        else:
            response = {
                'status': 'fail',
                'message': 'Flight not available. ',
            }
            return make_response(jsonify(response)), 400


class ReservationsView(MethodView):
    decorators = [token_required]

    @token_required
    @admin_required
    def get(self, current_user):
        all_flights = Flight.fetch_all()
        all_bookings = Booking.fetch_all()
        days = list(set([item.created_at.strftime('%D')
                         for item in all_bookings]))
        reservations_per_day = {}
        for day in days:
            flights = []
            for flight in all_flights:
                date = datetime.strptime(day, '%m/%d/%y')
                booked_flights = Booking.filter(
                    Booking.flight_id == (flight.id)).filter(
                    extract('day', Booking.created_at) == date.day).all()
                users = set()
                [users.add(booking.user_id) for booking in booked_flights]
                booked_flight = {(flight.flight_number): {
                    'Number of users': len(users),
                    'Number of bookings': len(booked_flights),
                    'Bookings': [
                        flight.serialize() for flight in booked_flights]
                }

                }
                flights.append(booked_flight)
            reservations_per_day.update({day: flights})

        response = {
            'status': 'success',
            'flights': reservations_per_day
        }
        return make_response(jsonify(response)), 200
