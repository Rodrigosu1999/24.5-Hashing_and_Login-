"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Users Model."""

    __tablename__ = "users"

    username = db.Column(db.String(20),
                         primary_key=True)
    password = db.Column(db.String,
                         nullable=False)
    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Functionality for registering a new instance of User"""
        hashed_pw = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed_pw.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that the user exist and that the password is correct"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Feedback(db.Model):
    """Feedback Model."""

    __tablename__ = "feedback"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.String,
                        nullable=False)
    username = db.Column(db.String(20),
                         db.ForeignKey("users.username"))

    user = db.relationship("User", backref="feedback",
                           cascade="all, delete-orphan",
                           single_parent=True)
