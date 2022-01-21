from werkzeug import security
from flask_login import UserMixin
from flask_sqlalchemy import BaseQuery
from klee_engine.application import db, login_manager
from klee_engine.models.exceptions import WrongPassword, UserNotFound


@login_manager.user_loader
def get_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120))
    experiments = db.relationship(
        argument="Experiment", backref="users", lazy=True
    )
    __tablename__ = "users"

    def __init__(self, email, password, name=None):
        self.password = security.generate_password_hash(password)
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.email}>'

    def verify_password(self, password):
        if not security.check_password_hash(self.password, password):
            raise WrongPassword


def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        raise UserNotFound

    return user
