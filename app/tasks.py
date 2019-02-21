import celery

from datetime import timedelta, datetime

from app import app
from app.models import Booking, Flight, User
from app.notifications import send_email


@celery.task()
def periodic_run():
    """ Perodic task, run by Celery Beat process """
    with app.app_context():
        all_bookings = Booking.fetch_all()
        for booking in all_bookings:
            flight = Flight.find_first(id=booking.flight_id)
            now = datetime.now()
            if now - timedelta(hours=24) <= flight.flight_date <= (
                    now + timedelta(hours=24)):
                if booking.reminder_sent is False:
                    user = User.find_first(id=booking.user_id)
                    booking.reminder_sent = True
                    booking.save()
                    send_email(
                        'Reminder', [user.email],
                        'Flight',
                        f'Hello {user.name}\n'
                        f'Your flight with {flight.flight_name} '
                        f'{flight.flight_number} is '
                        f'tommorrow at {flight.flight_date}')
        return 'success'
