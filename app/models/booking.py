from datetime import datetime

from .model_mixin import ModelMixin, db


class Booking(ModelMixin):
    """
    Booking model atttributes
    """
    __tablename__ = 'booking'

    flight_number = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)
    flight_id = db.Column(db.Integer, db.ForeignKey(
        'flight.id'), nullable=False)
    flight = db.relationship("Flight", back_populates="bookings")
