from .model_mixin import db, ModelMixin


class Flight(ModelMixin):
    """
    Flight model atttributes
    """
    __tablename__ = 'flight'

    flight_number = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="flight")
