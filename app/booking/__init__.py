from flask import Blueprint

from .views import BookingView, ReservationsView

booking_blueprint = Blueprint('booking', __name__, url_prefix='/api/v1')
booking_view = BookingView.as_view('booking_api')
booking_blueprint.add_url_rule(
    '/booking',
    view_func=booking_view,
    methods=['GET', 'POST']
)

reservation_view = ReservationsView.as_view('reservation_api')
booking_blueprint.add_url_rule(
    '/booking/reserve',
    view_func=reservation_view,
    methods=['GET']
)
