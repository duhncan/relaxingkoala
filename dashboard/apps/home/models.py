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
    status = db.Column(db.String(50), nullable=False, default="Pending")
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    type = db.Column(db.String(50))

    __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "payment"}


class CashPayment(Payment):
    __tablename__ = "cash_payment"
    id = db.Column(db.Integer, db.ForeignKey("payment.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "cash",
    }


class CardPayment(Payment):
    __tablename__ = "card_payment"
    id = db.Column(db.Integer, db.ForeignKey("payment.id"), primary_key=True)
    card_number = db.Column(db.String(20), nullable=False)
    card_expiration_date = db.Column(db.String(7), nullable=False)
    card_cvv = db.Column(db.String(4), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "card",
    }


order_items = db.Table(
    "order_items",
    db.Column("order_id", db.Integer, db.ForeignKey("order.id"), primary_key=True),
    db.Column(
        "menu_item_id", db.Integer, db.ForeignKey("menu_item.id"), primary_key=True
    ),
)


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_file = db.Column(
        db.String(100), nullable=True, default="default.jpg"
    )  # Add this line

    def __repr__(self):
        return f"MenuItem('{self.name}', '{self.price}', '{self.image_file}')"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    total_amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(50), nullable=False, default="Pending")
    items = db.relationship(
        "MenuItem", secondary=order_items, backref="orders", lazy="dynamic"
    )
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    delivery_option = db.Column(db.String(50), nullable=False, default="Pickup")  
    delivery_status = db.Column(db.String(50), nullable=False, default="Pending")  


class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    seats = db.Column(db.Integer, nullable=False)
    reservations = db.relationship("Reservation", backref="table", lazy=True)


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey("table.id"), nullable=False)
    reservation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
