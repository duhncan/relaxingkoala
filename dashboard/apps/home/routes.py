# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from apps.home import blueprint
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_required
from jinja2 import TemplateNotFound
import os

from apps.authentication.models import Users
from apps.authentication.forms import CreateAccountForm
from apps.home.models import *
from apps.home.forms import *
from apps.home.utils import save_picture, delete_picture


@blueprint.route("/index")
@login_required
def index():
    return render_template("pages/index.html", segment="index")


@blueprint.route("/home-page")
@login_required
def home_page():
    return render_template("pages/home-page.html")


@blueprint.route("/table-page")
@login_required
def table_page():
    return render_template("pages/table-page.html")


@blueprint.route("/accounts/password-reset/")
def password_reset():
    return render_template("accounts/password_reset.html")


@blueprint.route("/accounts/password-reset-done/")
def password_reset_done():
    return render_template("accounts/password_reset_done.html")


@blueprint.route("/accounts/password-reset-confirm/")
def password_reset_confirm():
    return render_template("accounts/password_reset_confirm.html")


@blueprint.route("/accounts/password-reset-complete/")
def password_reset_complete():
    return render_template("accounts/password_reset_complete.html")


@blueprint.route("/accounts/password-change/")
def password_change():
    return render_template("accounts/password_change.html")


@blueprint.route("/accounts/password-change-done/")
def password_change_done():
    return render_template("accounts/password_change_done.html")


"""
Customary Pages
"""
@blueprint.route("/contact")
def contact():
    return render_template("pages/about_us.html")


@blueprint.route("/about")
def about():
    return render_template("pages/contact_us.html")



"""
Menu Related
"""


@blueprint.route("/menu")
def menu_items():
    items = MenuItem.query.all()
    return render_template("pages/menu.html", items=items)


@blueprint.route("/menu/add_item", methods=["GET", "POST"])
def new_menu_item():
    form = MenuItemForm()
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data, output_size=(300, 300))
        else:
            picture_file = "default.jpg"
        menu_item = MenuItem(
            name=form.name.data, price=form.price.data, image_file=picture_file
        )
        db.session.add(menu_item)
        db.session.commit()
        flash("Menu item has been created!", "success")
        return redirect(url_for("home_blueprint.menu_items"))
    return render_template("pages/add_menu_item.html", title="New Menu Item", form=form)


@blueprint.route("/menu/manage", methods=["GET", "POST"])
def manage_menu_items():
    items = MenuItem.query.all()
    return render_template("pages/manage_menu_items.html", items=items)


@blueprint.route("/menu/delete/<int:item_id>", methods=["POST"])
def delete_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    if item.image_file != "default.jpg":
        picture_path = delete_picture(item.image_file)
    db.session.delete(item)
    db.session.commit()
    flash("Menu item has been deleted!", "success")
    return redirect(url_for("home_blueprint.manage_menu_items"))


"""
Payment & Ordering
"""


@blueprint.route("/confirmation/<int:order_id>")
def confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template("pages/order_confirmation.html", order=order)


@blueprint.route("/order/<int:order_id>/payment", methods=["GET", "POST"])
def payment(order_id):
    # Retrieve the order from the database
    order = Order.query.get_or_404(order_id)

    # Check if the order has already been paid
    if order.payment_status == "Paid":
        flash("This order has already been paid.", "warning")
        return redirect(url_for("home_blueprint.confirmation", order_id=order_id))

    # Handle the payment process for both cash and card
    cash_form = CashPaymentForm()
    card_form = CardPaymentForm()
    if request.form.get("payment_type") == "cash":
        if cash_form.validate_on_submit():
            # Check if the payment method matches 'cash'
            # Handle Cash Payment
            payment = CashPayment(
                payer_name=cash_form.payer_name.data,
                email=cash_form.email.data,
                amount=order.total_amount,
                status="Completed",
                payment_date=datetime.utcnow(),
                order_id=order.id,
            )
            order.payment_status = "Paid"
            db.session.add(payment)
            db.session.commit()
            flash("Cash payment made successfully!", "success")
            return redirect(url_for("home_blueprint.confirmation", order_id=order_id))
        else:
            for field, errors in cash_form.errors.items():
                for error in errors:
                    flash(f"Error in {field}: {error}", "danger")
    elif request.form.get("payment_type") == "card":
        if card_form.validate_on_submit():
            # Check if the payment method matches 'card'
            # Handle Card Payment
            payment = CardPayment(
                payer_name=card_form.payer_name.data,
                email=card_form.email.data,
                amount=order.total_amount,
                status="Completed",
                payment_date=datetime.utcnow(),
                order_id=order.id,
                card_number=card_form.card_number.data,
                card_expiration_date=card_form.card_expiration_date.data,
                card_cvv=card_form.card_cvv.data,
            )
            order.payment_status = "Paid"
            db.session.add(payment)
            db.session.commit()
            flash("Card payment made successfully!", "success")
            return redirect(url_for("home_blueprint.confirmation", order_id=order_id))
        else:
            for field, errors in card_form.errors.items():
                for error in errors:
                    flash(f"Error in {field}: {error}", "danger")
    else:
        flash(f"Error submitting payment", "danger")

    return render_template(
        "pages/payment.html", order=order, cash_form=cash_form, card_form=card_form
    )


@blueprint.route("/order/create", methods=["GET", "POST"])
def create_order():
    items = MenuItem.query.all()
    form = OrderForm()
    form.items.choices = [
        (item.id, f"{item.name} - ${item.price}") for item in MenuItem.query.all()
    ]
    if form.validate_on_submit():
        items = MenuItem.query.filter(MenuItem.id.in_(form.items.data)).all()
        total_amount = sum(item.price for item in items)
        order = Order(
            customer_name=form.customer_name.data,
            email=form.email.data,
            phone_number=form.phone_number.data
            if form.phone_number.data
            else None,  # Handle optional phone number
            items=items,
            total_amount=total_amount,
            delivery_option=form.delivery_option.data,
        )
        db.session.add(order)
        db.session.commit()
        flash("Order placed successfully! Redirecting to payment page...", "success")
        # Redirect the user to the payment page
        return redirect(url_for("home_blueprint.payment", order_id=order.id))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    f"Error in the {getattr(form, field).label.text} field - {error}",
                    "danger",
                )
    return render_template("pages/create_order.html", form=form, menu_items=items)


@blueprint.route("/orders")
def list_orders():
    orders = Order.query.all()
    return render_template("pages/list_orders.html", orders=orders)


@blueprint.route('/order/<int:order_id>/pickup', methods=['POST'])
def pickup_order(order_id):
    order = Order.query.get_or_404(order_id)
    order.delivery_status = "Picked Up"
    db.session.commit()
    flash("Order picked up by driver!", "success")
    return render_template("pages/delivery.html", order_id=order.id)

"""
Reservation & Tables
"""

@blueprint.route("/add_table", methods=["GET", "POST"])
def add_table():
    form = TableForm()
    if form.validate_on_submit():
        table = Table(number=form.number.data, seats=form.seats.data)
        db.session.add(table)
        db.session.commit()
        flash("Table added successfully!", "success")
        return redirect(url_for(".add_table"))
    return render_template("pages/add_table.html", form=form)


@blueprint.route("/reserve_table", methods=["GET", "POST"])
def reserve_table():
    form = ReservationForm()
    form.table_id.choices = [
        (table.id, f"Table {table.number} - {table.seats} seats")
        for table in Table.query.all()
    ]
    if form.validate_on_submit():
        try:
            reservation_date = datetime.utcnow().date()
            reservation_time_str = form.reservation_time.data
            reservation_datetime = datetime.strptime(
                f"{reservation_date} {reservation_time_str}", "%Y-%m-%d %H:%M"
            )
            reservation = Reservation(
                customer_name=form.customer_name.data,
                email=form.email.data,
                phone_number=form.phone_number.data,
                table_id=form.table_id.data,
                reservation_time=reservation_datetime,
            )
            db.session.add(reservation)
            db.session.commit()
            flash("Table reserved successfully!", "success")
            return redirect(url_for(".reserve_table"))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    f"Error in the {getattr(form, field).label.text} field - {error}",
                    "danger",
                )
    return render_template("pages/reserve_table.html", form=form)

@blueprint.route("/reservation_submit", methods=["POST"])
def reservation_submit():
    # Extract form data
    date = request.form.get("date")
    time = request.form.get("time")
    people = request.form.get("people")
    name = request.form.get("name")
    phone = request.form.get("phone")
    return redirect(url_for("home_blueprint.table_page"))


@blueprint.route("/available_tables")
def available_tables():
    reservations = Reservation.query.filter(
        Reservation.reservation_time >= datetime.utcnow()
    ).all()
    reserved_table_ids = [reservation.table_id for reservation in reservations]
    available_tables = Table.query.filter(~Table.id.in_(reserved_table_ids)).all()
    return render_template("pages/available_tables.html", tables=available_tables)

"""
Manager Functions
"""


@blueprint.route('/manager/users', methods=['GET', 'POST'])
@login_required
def manage_users():
    users = Users.query.all()
    create_account_form = CreateAccountForm(request.form)
    if request.method == 'POST':
        user_id = request.form['user_id']
        new_role = request.form['role']
        user = Users.query.get(user_id)
        if user:
            user.role = new_role
            db.session.commit()
            flash('User role updated successfully', 'success')
        else:
            flash('User not found', 'danger')
        return redirect(url_for('manage_users'))

    return render_template('pages/manage_users.html', users=users, form=create_account_form)

@blueprint.route('/manager/reports', methods=['GET', 'POST'])
@login_required
def manager_reports():
    return render_template('pages/report-page.html')


@blueprint.route("/<template>")
@login_required
def route_template(template):
    try:
        if not template.endswith(".html"):
            template += ".html"

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template("home/page-404.html"), 404

    except:
        return render_template("home/page-500.html"), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split("/")[-1]

        if segment == "":
            segment = "index"

        return segment

    except:
        return None
