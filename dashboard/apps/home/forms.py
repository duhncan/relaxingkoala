from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    FloatField,
    HiddenField,
    DateTimeField,
    SelectMultipleField,
    IntegerField,
    SelectField,
    FileField,
)
from wtforms.validators import DataRequired, Email, NumberRange, Length, Optional
from flask_wtf.file import FileAllowed


class PaymentForm(FlaskForm):
    payer_name = StringField("Payer Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    amount = FloatField("Amount", validators=[DataRequired()])
    payment_type = SelectField(
        "Payment Type",
        choices=[("cash", "Cash"), ("card", "Card")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Make Payment")


class CashPaymentForm(PaymentForm):
    pass


class CardPaymentForm(PaymentForm):
    card_number = StringField(
        "Card Number", validators=[DataRequired(), Length(min=16, max=16)]
    )
    card_expiration_date = StringField(
        "Card Expiration Date (MM/YYYY)",
        validators=[DataRequired(), Length(min=7, max=7)],
    )
    card_cvv = StringField("CVV", validators=[DataRequired(), Length(min=3, max=4)])


class MenuItemForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired(), NumberRange(min=0)])
    image_file = FileField("Update Image", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Save")


class OrderForm(FlaskForm):
    customer_name = StringField("Customer Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone_number = StringField("Phone Number", validators=[Optional()])
    items = SelectMultipleField("Menu Items", coerce=int, validators=[DataRequired()])
    delivery_option = SelectField(
        "Delivery Option",
        choices=[("Dine-in", "Dine-in"), ("Pickup", "Pickup"), ("Delivery", "Delivery")],
        validators=[DataRequired()]
    )
    submit = SubmitField("Place Order")


class TableForm(FlaskForm):
    number = IntegerField("Table Number", validators=[DataRequired()])
    seats = IntegerField("Number of Seats", validators=[DataRequired()])
    submit = SubmitField("Add Table")


class ReservationForm(FlaskForm):
    customer_name = StringField("Customer Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone_number = StringField(
        "Phone Number", validators=[DataRequired(), Length(min=10, max=20)]
    )
    table_id = SelectField("Table", coerce=int, validators=[DataRequired()])
    reservation_time = SelectField(
        "Reservation Time",
        choices=[
            ("12:00", "12:00 PM"),
            ("12:30", "12:30 PM"),
            ("13:00", "1:00 PM"),
            ("13:30", "1:30 PM"),
            ("14:00", "2:00 PM"),
            ("14:30", "2:30 PM"),
            ("15:00", "3:00 PM"),
            ("15:30", "3:30 PM"),
            ("16:00", "4:00 PM"),
            ("16:30", "4:30 PM"),
            ("17:00", "5:00 PM"),
            ("17:30", "5:30 PM"),
            ("18:00", "6:00 PM"),
            ("18:30", "6:30 PM"),
            ("19:00", "7:00 PM"),
            ("19:30", "7:30 PM"),
            ("20:00", "8:00 PM"),
            ("20:30", "8:30 PM"),
            ("21:00", "9:00 PM"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Reserve Table")


class OrderSearchForm(FlaskForm):
    search_query = StringField(
        "Enter your name, email, or phone number", validators=[DataRequired()]
    )
    submit = SubmitField("Search")


class OrderSelectionForm(FlaskForm):
    order_id = SelectField("Select Order", coerce=int, validators=[DataRequired()])
    payment_type = SelectField(
        "Payment Type",
        choices=[("cash", "Cash"), ("card", "Card")],
        validators=[DataRequired()],
    )
    payer_name = StringField("Payer Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Proceed to Payment")

