from gino import Gino
from sqlalchemy import func

db = Gino()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    telegram_user_id = db.Column(db.String(length=200))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    first_name = db.Column(db.String(length=255))
    last_name = db.Column(db.String(length=255))
    username = db.Column(db.String(length=255))


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.String())
    result = db.Column(db.String())
    started_at = db.Column(db.DateTime(timezone=True), default=func.now())
    ended_at = db.Column(db.DateTime(timezone=True))
    periods = db.Column(db.Integer, db.ForeignKey('periods.id'))


class Period(db.Model):
    __tablename__ = 'periods'

    id = db.Column(db.Integer, primary_key=True)
    started_at = db.Column(db.DateTime(timezone=True), default=func.now())
    ended_at = db.Column(db.DateTime(timezone=True))