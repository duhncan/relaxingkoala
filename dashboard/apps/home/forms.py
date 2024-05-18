from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, HiddenField, DateTimeField, SelectMultipleField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, NumberRange


class PaymentForm(FlaskForm):
    payer_name = StringField('Payer Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    amount = HiddenField('Amount', validators=[DataRequired()])
    submit = SubmitField('Submit Payment')

class MenuItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    submit = SubmitField('Add Menu Item')

class OrderForm(FlaskForm):
    customer_name = StringField('Customer Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    items = SelectMultipleField('Menu Items', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Place Order')

class TableForm(FlaskForm):
    number = IntegerField('Table Number', validators=[DataRequired()])
    seats = IntegerField('Number of Seats', validators=[DataRequired()])
    submit = SubmitField('Add Table')

class ReservationForm(FlaskForm):
    customer_name = StringField('Customer Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    table_id = SelectField('Table', coerce=int, validators=[DataRequired()])
    reservation_time = SelectField('Reservation Time', choices=[
        ('12:00', '12:00 PM'),
        ('12:30', '12:30 PM'),
        ('13:00', '1:00 PM'),
        ('13:30', '1:30 PM'),
        ('14:00', '2:00 PM'),
        ('14:30', '2:30 PM'),
        ('15:00', '3:00 PM'),
        ('15:30', '3:30 PM'),
        ('16:00', '4:00 PM'),
        ('16:30', '4:30 PM'),
        ('17:00', '5:00 PM'),
        ('17:30', '5:30 PM'),
        ('18:00', '6:00 PM'),
        ('18:30', '6:30 PM'),
        ('19:00', '7:00 PM'),
        ('19:30', '7:30 PM'),
        ('20:00', '8:00 PM'),
        ('20:30', '8:30 PM'),
        ('21:00', '9:00 PM')
    ], validators=[DataRequired()])
    submit = SubmitField('Reserve Table')