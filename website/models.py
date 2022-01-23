from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    predictions = db.relationship('Prediction')

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    event = db.Column(db.String(1000))
    rider_one = db.Column(db.String(1000))
    rider_two = db.Column(db.String(1000))
    rider_three = db.Column(db.String(1000))
    user_name = db.Column(db.String(1000), db.ForeignKey('user.name'))
