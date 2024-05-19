# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from apps.home import blueprint
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_required
from jinja2 import TemplateNotFound
import os

from apps.home.models import *
from apps.home.forms import *
from apps.home.utils import save_picture, delete_picture

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
Menu Related
"""

@blueprint.route('/menu')
def menu_items():
    items = MenuItem.query.all()
    return render_template('pages/menu.html', items=items)

@blueprint.route('/menu/add_item', methods=['GET', 'POST'])
def new_menu_item():
    form = MenuItemForm()
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data, output_size=(300, 300))
        else:
            picture_file = 'default.jpg'
        menu_item = MenuItem(name=form.name.data, price=form.price.data, image_file=picture_file)
        db.session.add(menu_item)
        db.session.commit()
        flash('Menu item has been created!', 'success')
        return redirect(url_for('home_blueprint.menu_items'))
    return render_template('pages/add_menu_item.html', title='New Menu Item', form=form)

@blueprint.route('/menu/manage', methods=['GET', 'POST'])
def manage_menu_items():
    items = MenuItem.query.all()
    return render_template('pages/manage_menu_items.html', items=items)

@blueprint.route('/menu/delete/<int:item_id>', methods=['POST'])
def delete_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    if item.image_file != 'default.jpg':
        picture_path = delete_picture(item.image_file)
    db.session.delete(item)
    db.session.commit()
    flash('Menu item has been deleted!', 'success')
    return redirect(url_for('home_blueprint.manage_menu_items'))

"""
Payment
"""
@blueprint.route('/make_payment', methods=['GET', 'POST'])
def make_payment():
    search_form = OrderSearchForm()
    order_form = OrderSelectionForm()
    orders = []

    if search_form.validate_on_submit():
        search_query = search_form.search_query.data
        orders = Order.query.filter(
            (Order.customer_name.ilike(f"%{search_query}%")) |
            (Order.email.ilike(f"%{search_query}%"))
        ).all()
        
        if not orders:
            flash('No orders found for the given details.', 'danger')
        else:
            order_form.order_id.choices = [(order.id, f"Order #{order.id} - ${order.total_amount}") for order in orders]
            return render_template('pages/select_order.html', search_form=search_form, order_form=order_form, orders=orders)

    if order_form.validate_on_submit():
        order = Order.query.get(order_form.order_id.data)
        if not order:
            flash('Order not found.', 'danger')
            return redirect(url_for('.make_payment'))

        if order_form.payment_type.data == 'cash':
            payment = CashPayment(
                payer_name=order_form.payer_name.data,
                email=order_form.email.data,
                amount=order.total_amount,
                status='Completed',
                payment_date=datetime.utcnow(),
                order_id=order.id
            )
            order.payment_status = 'Paid'
            db.session.add(payment)
            db.session.commit()
            flash('Cash payment made successfully!', 'success')
            return redirect(url_for('.make_payment'))

        elif order_form.payment_type.data == 'card':
            card_form = CardPaymentForm()
            if card_form.validate_on_submit():
                payment = CardPayment(
                    payer_name=order_form.payer_name.data,
                    email=order_form.email.data,
                    amount=order.total_amount,
                    status='Completed',
                    payment_date=datetime.utcnow(),
                    order_id=order.id,
                    card_number=card_form.card_number.data,
                    card_expiration_date=card_form.card_expiration_date.data,
                    card_cvv=card_form.card_cvv.data
                )
                order.payment_status = 'Paid'
                db.session.add(payment)
                db.session.commit()
                flash('Card payment made successfully!', 'success')
                return redirect(url_for('.make_payment'))
            else:
                flash('Card payment details are invalid.', 'danger')
                return render_template('pages/select_order.html', search_form=search_form, order_form=order_form, card_form=card_form)

    return render_template('pages/make-payment.html', search_form=search_form, order_form=order_form, orders=orders)


@blueprint.route('/confirmation/<int:order_id>')
def confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('pages/confirmation.html', order=order)


"""
Ordering
"""

@blueprint.route('/order/<float:order_amount>')
def order(order_amount):
    return redirect(url_for('payment', amount=order_amount))


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
            phone_number=form.phone_number.data if form.phone_number.data else None,  # Handle optional phone number
            items=items,
            total_amount=total_amount
        )
        db.session.add(order)
        db.session.commit()
        flash('Order placed successfully!', 'success')
        return redirect(url_for('home_blueprint.confirmation', order_id=order.id))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in the {getattr(form, field).label.text} field - {error}", 'danger')
    return render_template('pages/create_order.html', form=form)

@blueprint.route('/orders')
def list_orders():
    orders = Order.query.all()
    return render_template('pages/list_orders.html', orders=orders)


"""
Reservation & Tables
"""

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
                phone_number=form.phone_number.data,
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
