from .model_mixin import db, ModelMixin


class Flight(ModelMixin):
    """
    Flight model atttributes
    """
    __tablename__ = 'flight'

    flight_number = db.Column(db.String(120), unique=True, nullable=False)
    capacity = db.Column(db.Integer, default=62)
    bookings = db.relationship("Booking", backref="flight", lazy="dynamic")
