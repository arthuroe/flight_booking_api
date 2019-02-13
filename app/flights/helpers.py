from app.models import Booking, Flight


def get_available_flights():
    all_flights = Flight.fetch_all()
    all_bookings = Booking.fetch_all()
    available = []
    for flight in all_flights:
        if check_flight_is_available(flight):
            available.append(flight)
    return available


def check_flight_is_available(flight):
    bookings = Booking.filter(flight.id)
    if flight.capacity < len(bookings):
        return True
    return False
