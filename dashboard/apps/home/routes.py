# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from apps.home import blueprint
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_required
from jinja2 import TemplateNotFound

from apps import db
from apps.home.models import *
from apps.home.forms import *

@blueprint.route('/index')
@login_required
def index():
    return render_template('pages/index.html', segment='index')

@blueprint.route('/typography')
@login_required
def typography():
    return render_template('pages/typography.html')

@blueprint.route('/color')
@login_required
def color():
    return render_template('pages/color.html')

@blueprint.route('/icon-tabler')
@login_required
def icon_tabler():
    return render_template('pages/icon-tabler.html')

@blueprint.route('/sample-page')
@login_required
def sample_page():
    return render_template('pages/sample-page.html')  

@blueprint.route('/home-page')
@login_required
def home_page():
    return render_template('pages/home-page.html')  

@blueprint.route('/order-page')
@login_required
def order_page():
    return render_template('pages/order-page.html')  

@blueprint.route('/menu-page')
@login_required
def menu_page():
    return render_template('pages/menu-page.html')  

@blueprint.route('/reservation-page')
@login_required
def reservation_page():
    return render_template('pages/reservation-page.html')

@blueprint.route('/reservation_submit', methods=['POST'])
@login_required
def reservation_submit():
    # Extract form data
    date = request.form.get('date')
    time = request.form.get('time')
    people = request.form.get('people')
    name = request.form.get('name')
    phone = request.form.get('phone')
    

    
    return redirect(url_for('home_blueprint.table_page'))

@blueprint.route('/table-page')
@login_required
def table_page():
    return render_template('pages/table-page.html')  

@blueprint.route('/report-page')
@login_required
def report_page():
    return render_template('pages/report-page.html')  

def get_report(report_type):
    if report_type == 'sales':
        data = [{'Month': 'January', 'Revenue': 10000}, {'Month': 'February', 'Revenue': 15000}]
    elif report_type == 'items_sold':
        data = [{'Item': 'Widget', 'Sold': 120}, {'Item': 'Gadget', 'Sold': 90}]
    else:
        data = []
    return jsonify(data)

@blueprint.route('/accounts/password-reset/')
def password_reset():
    return render_template('accounts/password_reset.html')

@blueprint.route('/accounts/password-reset-done/')
def password_reset_done():
    return render_template('accounts/password_reset_done.html')

@blueprint.route('/accounts/password-reset-confirm/')
def password_reset_confirm():
    return render_template('accounts/password_reset_confirm.html')

@blueprint.route('/accounts/password-reset-complete/')
def password_reset_complete():
    return render_template('accounts/password_reset_complete.html')

@blueprint.route('/accounts/password-change/')
def password_change():
    return render_template('accounts/password_change.html')

@blueprint.route('/accounts/password-change-done/')
def password_change_done():
    return render_template('accounts/password_change_done.html')

"""
Report
"""


"""
Payment
"""
@blueprint.route('/payment/<float:amount>', methods=['GET', 'POST'])
def payment(amount):
    form = PaymentForm(amount=amount)
    if form.validate_on_submit():
        payment = Payment(
            payer_name=form.payer_name.data,
            email=form.email.data,
            amount=form.amount.data,
            status='Confirmed'
        )
        db.session.add(payment)
        db.session.commit()
        flash('Payment successfully processed!', 'success')
        return redirect(url_for('confirmation', payment_id=payment.id))
    return render_template('pages/payment.html', form=form, amount=amount)


@blueprint.route('/confirmation/<int:order_id>')
def confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('pages/confirmation.html', order=order)

@blueprint.route('/order/<float:order_amount>')
def order(order_amount):
    return redirect(url_for('payment', amount=order_amount))


@blueprint.route('/add_menu_item', methods=['GET', 'POST'])
def add_menu_item():
    form = MenuItemForm()
    if form.validate_on_submit():
        item = MenuItem(name=form.name.data, price=form.price.data)
        db.session.add(item)
        db.session.commit()
        flash('Menu item added successfully!', 'success')
        return redirect('/add_menu_item')
    return render_template('pages/add_menu_item.html', form=form)

@blueprint.route('/create_order', methods=['GET', 'POST'])
def create_order():
    form = OrderForm()
    form.items.choices = [(item.id, f"{item.name} - ${item.price}") for item in MenuItem.query.all()]
    if form.validate_on_submit():
        items = MenuItem.query.filter(MenuItem.id.in_(form.items.data)).all()
        total_amount = sum(item.price for item in items)
        order = Order(
            customer_name=form.customer_name.data,
            email=form.email.data,
            items=items,
            total_amount=total_amount
        )
        db.session.add(order)
        db.session.commit()
        flash('Order placed successfully!', 'success')
        return redirect(url_for('pages/confirmation', order_id=order.id))
    else:
        # If the form is not valid, flash error messages
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in the {getattr(form, field).label.text} field - {error}", 'danger')
    return render_template('pages/create_order.html', form=form)

@blueprint.route('/orders')
def list_orders():
    orders = Order.query.all()
    return render_template('pages/list_orders.html', orders=orders)



@blueprint.route('/add_table', methods=['GET', 'POST'])
def add_table():
    form = TableForm()
    if form.validate_on_submit():
        table = Table(number=form.number.data, seats=form.seats.data)
        db.session.add(table)
        db.session.commit()
        flash('Table added successfully!', 'success')
        return redirect(url_for('.add_table'))
    return render_template('pages/add_table.html', form=form)

@blueprint.route('/reserve_table', methods=['GET', 'POST'])
def reserve_table():
    form = ReservationForm()
    form.table_id.choices = [(table.id, f"Table {table.number} - {table.seats} seats") for table in Table.query.all()]
    if form.validate_on_submit():
        try:
            reservation_date = datetime.utcnow().date()
            reservation_time_str = form.reservation_time.data
            reservation_datetime = datetime.strptime(f"{reservation_date} {reservation_time_str}", "%Y-%m-%d %H:%M")
            reservation = Reservation(
                customer_name=form.customer_name.data,
                email=form.email.data,
                table_id=form.table_id.data,
                reservation_time=reservation_datetime
            )
            db.session.add(reservation)
            db.session.commit()
            flash('Table reserved successfully!', 'success')
            return redirect(url_for('.reserve_table'))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in the {getattr(form, field).label.text} field - {error}", 'danger')
    return render_template('pages/reserve_table.html', form=form)

@blueprint.route('/available_tables')
def available_tables():
    reservations = Reservation.query.filter(Reservation.reservation_time >= datetime.utcnow()).all()
    reserved_table_ids = [reservation.table_id for reservation in reservations]
    available_tables = Table.query.filter(~Table.id.in_(reserved_table_ids)).all()
    return render_template('pages/available_tables.html', tables=available_tables)

"""
Reservation
"""



@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
