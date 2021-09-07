import os
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

from sqlalchemy.orm import backref
from sqlalchemy.sql.expression import true
from datetime import datetime

# Models will include at least:
# 1- Two classes with primary keys at at least two attributes each
# 2- [Optional but encouraged] One-to-many or many-to-many relationships between classes

database_name = "resturant"
database_path = "postgresql://postgres:1998@{}/{}".format(
    'localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):

    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

    Migrate(app, db)


class user(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))

    order = db.relationship('order', backref='user', lazy=True)

    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def information(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
        }


class order(db.Model):
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)
    quantity = db.Column(db.Integer)
    order_time = db.Column(db.DateTime)
    pickup_time = db.Column(db.DateTime)

    def __init__(self, user_id, pizza_id, quantity, order_time, pickup_time):
        self.user_id = user_id
        self.pizza_id = pizza_id
        self.quantity = quantity
        self.order_time = order_time
        self.pickup_time = pickup_time

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def information(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "pizza_id": self.pizza_id,
            "quantity": self.quantity,
            "order_time": self.order_time.strftime("%m/%d/%Y, %H:%M:%S"),
            "pickup_time": self.pickup_time.strftime("%m/%d/%Y, %H:%M:%S")
        }


class pizza(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    ingredients = db.Column(db.String(500))

    order = db.relationship('order', backref='pizza', lazy=True)

    def __init__(self, name, price, ingredients):
        self.name = name
        self.price = price
        self.ingredients = ingredients

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def information(self):
        return {
            "id":self.id,
            "name": self.name,
            "price": self.price,
            "ingredients": self.ingredients
        }
