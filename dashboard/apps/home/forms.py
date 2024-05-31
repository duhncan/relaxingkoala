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

from datetime import datetime, time, timedelta


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

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        
        # Generate choices for reservation time based on current date and time
        self.reservation_time.choices = self.generate_reservation_time_choices()

    def generate_reservation_time_choices(self):
        # Get current date and time
        current_date = datetime.now().date()
        current_time = datetime.now().time()

        # Calculate the end date for the booking window (2 weeks in advance)
        end_date = current_date + timedelta(days=14)

        # Set the start and end times for reservations (9 AM to 9 PM)
        start_time = time(9, 0)
        end_time = time(21, 0)

        # If current time is before 9 AM, start from 9 AM of the current day
        if current_time < start_time:
            current_datetime = datetime.combine(current_date, start_time)
        # If current time is after 9 PM, start from 9 AM of the next day
        elif current_time >= end_time:
            current_date += timedelta(days=1)
            current_datetime = datetime.combine(current_date, start_time)
        # Otherwise, start from the next half-hour slot
        else:
            current_datetime = datetime.combine(current_date, current_time)
            current_datetime += timedelta(minutes=(30 - current_datetime.minute % 30))

        choices = []

        # Generate choices from current time to 9 PM for dates within the booking window
        while current_date <= end_date:
            # Only add times for the current date if it's within the booking window
            if current_date == end_date or current_date < end_date:
                # Include both date and time in the choice tuple
                choice = (current_datetime.strftime('%Y-%m-%d %H:%M'), current_datetime.strftime('%d/%m/%Y %I:%M %p'))
                choices.append(choice)
            current_datetime += timedelta(minutes=30)
            if current_datetime.time() >= end_time:
                current_date += timedelta(days=1)
                current_datetime = datetime.combine(current_date, start_time)

        return choices

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

