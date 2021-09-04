import os
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

from sqlalchemy.orm import backref
from sqlalchemy.sql.expression import true


# Models will include at least:
# 1- Two classes with primary keys at at least two attributes each
# 2- [Optional but encouraged] One-to-many or many-to-many relationships between classes

database_name = "resturant"
database_path = "postgresql://postgres:1998@{}/{}".format('localhost:5432', database_name)

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

class order(db.Model):
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, db.ForeignKey('user.id'))
    pizza_id = db.Column(Integer, db.ForeignKey('pizza.id')) 
    quantity = db.Column(db.Integer)
    order_time = db.Column(db.DateTime)
    pickup_time = db.Column(db.DateTime)

    user = db.relationship('user', backref='order', lazy=True)
    pizza = db.relationship('pizza', backref='order', lazy=True)

    

class pizza(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    ingredients = db.Column(db.String(500))

    order = db.relationship('order', backref='pizza', lazy=True)