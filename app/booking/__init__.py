from flask import Blueprint

from .views import BookingView

booking_blueprint = Blueprint('booking', __name__, url_prefix='/api/v1')
booking_view = BookingView.as_view('booking_api')
booking_blueprint.add_url_rule(
    '/booking',
    view_func=booking_view,
    methods=['GET', 'POST']
)
