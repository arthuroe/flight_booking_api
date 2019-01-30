from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from app import app


db = SQLAlchemy()


class ModelMixin(db.Model):
    """Base models.

    - Contains the serialize method to convert objects to a dictionary
    - Save and Delete utilities
    - Common field atrributes in the models
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    def serialize(self):
        """Map model objects to dict representation."""
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}

    def save(self):
        """Save an instance of the model to the database."""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    def __repr__(self):
        """REPL representation of model instance."""
        string_representation = self.__str__().replace("{", "(").replace(
            "}", ")").replace(":", "=")
        return f"{type(self).__name__}{string_representation}"

    def __str__(self):
        """String representation of model."""
        return str(self.serialize())

    def delete(self):
        """Delete an instance of the model from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    @classmethod
    def fetch_all(cls):
        """Return all the data in the model."""
        return cls.query.all()

    @classmethod
    def get(cls, *args):
        """Return data by the Id."""
        return cls.query.get(*args)

    @classmethod
    def count(cls):
        """Return the count of all the data in the model."""
        return cls.query.count()

    @classmethod
    def get_first_item(cls):
        """Return the first data in the model."""
        return cls.query.first()

    @classmethod
    def order_by(cls, *args):
        """Query and order the data of the model."""
        return cls.query.order_by(*args)

    @classmethod
    def filter_all(cls, **kwargs):
        """Query and filter the data of the model."""
        return cls.query.filter(**kwargs).all()

    @classmethod
    def filter_by(cls, **kwargs):
        """Query and filter the data of the model."""
        return cls.query.filter_by(**kwargs)

    @classmethod
    def find_first(cls, **kwargs):
        """Query and filter the data of a model, returning the first result."""
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def filter_and_order(cls, *args, **kwargs):
        """Query, filter and orders all the data of a model."""
        return cls.query.filter_by(**kwargs).order_by(*args)

    @classmethod
    def paginate(cls, **kwargs):
        """Query and paginate the data of a model, returning the first result."""
        return cls.query.paginate(**kwargs)

    @classmethod
    def filter(cls, *args):
        """Query and filter the data of the model."""
        return cls.query.filter(*args)

    def update(cls, **kwargs):
        """Update/merge an instance of the model."""
        try:
            if 'id' not in kwargs:
                return False

            _id = kwargs['id']

            record = cls.query.filter_by(id=_id).first()

            if record is None:
                return False

            for key, value in kwargs.items():
                setattr(record, key, value)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False
