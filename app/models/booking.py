from datetime import datetime

from .model_mixin import ModelMixin, db


class Booking(ModelMixin):
    """
    Booking model atttributes
    """
    __tablename__ = 'bookings'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)
    flight_id = db.Column(db.Integer, db.ForeignKey(
        'flights.id'), nullable=False)
