# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, redirect, url_for, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound

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
