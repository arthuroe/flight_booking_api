from datetime import datetime

from .model_mixin import db, ModelMixin


class Flight(ModelMixin):
    """
    Flight model atttributes
    """
    __tablename__ = 'flights'

    flight_name = db.Column(db.String(120), nullable=False)
    flight_number = db.Column(db.String(120), unique=True, nullable=False)
    flight_date = db.Column(db.DateTime, default=datetime.utcnow)
    flight_destination = db.Column(db.String(120), nullable=False)
    capacity = db.Column(db.Integer, default=62)
    bookings = db.relationship("Booking", backref="flights", lazy="dynamic")
