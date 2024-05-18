"""
  models.py
  ===================

  Description:          Models for the Relaxing Koala Restaraunt Management System. 
  Authors:              Duhncan Guy
  Creation Date:        2024-05-18
  Modification Date:    2024-05-18

"""
from apps import db
from datetime import datetime

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payer_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


order_items = db.Table('order_items',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('menu_item_id', db.Integer, db.ForeignKey('menu_item.id'), primary_key=True)
)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    orders = db.relationship('Order', secondary=order_items, back_populates='items')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    items = db.relationship('MenuItem', secondary=order_items, back_populates='orders')
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    seats = db.Column(db.Integer, nullable=False)
    reservations = db.relationship('Reservation', backref='table', lazy=True)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'), nullable=False)
    reservation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)