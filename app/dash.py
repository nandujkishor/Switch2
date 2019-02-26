import os, csv, json, datetime, requests
from app import app, login, mail
from flask import Blueprint, render_template, abort, redirect, request, url_for, jsonify
from jinja2 import TemplateNotFound
from config import Config
from app.forms import AddTalk, AddWorkshop, AddContest, MoreData, EduData, AddRegistration, AddonVolunteer
from app.models import User
from app.mail import farer_welcome_mail, amrsoy_reg_mail, testing_mail
from app.more import get_user_ip, access
from app.farer import staff_required
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from flask_login import login_user, current_user, logout_user, login_required

dash = Blueprint('dash', __name__)

@dash.route('/lounge/')
@login_required
@staff_required()
def lounge():
    users = requests.get(Config.HUB_URL+'/farer/user/count', headers={'Authorization':current_user.id})
    users = users.json()
    colleges = requests.get(Config.HUB_URL+'/farer/registered/college/count', headers={'Authorization':current_user.id})
    colleges = colleges.json()
    now = datetime.datetime.now().hour
    print(now)
    notification = "Meeting on the Student of the Year schools edition at N203 this Sunday. All team members are requested to be present."
    if now < 12:
        s = "Morning"
    if now >= 12:
        s = "Afternoon"
    if now > 16:
        s = "Evening"
    return render_template('dash/lounge.html',
                            user=current_user,
                            user_count=users.get('sub'),
                            colleges_count=colleges.get('sub'),
                            greeting=s,
                            notification=notification,
                            title="Switch Lounge"
                            )

@dash.route('/mc/maintenance/toggle/')
@login_required
@staff_required(5)
def mc_toggle_mtnc():
    Config.MAINTENANCE = not Config.MAINTENANCE
    return "Maintenance: " + Config.MAINTENANCE

@dash.route('/accounts/')
@login_required
@staff_required(5)
def accounts_home():

    user_arr = requests.get(Config.HUB_URL+'/farer/user/list/short')
    user_arr = user_arr.json()

    return render_template('dash/accounts.html', users = user_arr,
                            user=current_user,
                            count = len(user_arr),
                            title="Accounts control")

@dash.route('/pss/', methods=['GET','POST'])
@login_required
@staff_required(5)
def pss():
    form=PSS(request.form)
    if request.method == 'POST' and form.validate():
        return "Hello"
    return render_template('dash/pss.html', form=form)

def events_show(op, event):

    return render_template('dash/events.html',
                            event=event,
                            open=op,
                            title="Events Dashboard",
                            user=current_user)

@dash.route('/events/')
@dash.route('/events/talks')
@login_required
@staff_required()
def events_show_talks():
    
    return events_show(request.args.get('open'), "talks")

# Content to be pulled from the provided data endpoints

@dash.route('/events/workshops')
@login_required
@staff_required()
def events_show_workshops():

    return events_show(request.args.get('open'), "workshops")

@dash.route('/events/contests')
@login_required
@staff_required()
def events_show_contests():

    return events_show(request.args.get('open'), "contests")

@dash.route('/events/talks/add', methods=['GET'])
@login_required
# @staff_required("talks", 3)
def events_talk_add():

    print("GET Request for event addition")
    mode = request.args.get('m')

    if mode is not None:
        if mode == "1":
            form = AddTalk(request.form)
            return render_template('forms/dash/events/add_talk.html',
                                    form=form)
    else:
        return redirect(url_for('.events_show_talks', open=True))

    return jsonify(406)

@dash.route('/events/workshops/add/', methods=['GET'])
@login_required
# @staff_required("workshops", 3)
def events_workshop_add():

    print("GET Request for workshop addition")
    mode = request.args.get('m')

    if mode is not None:
        if mode == "1":
            form = AddWorkshop(request.form)
            return render_template('forms/dash/events/add_workshop.html',
                                    form=form)
    else:
        return redirect(url_for('.events_show_workshops', open=True))

    return jsonify(406)   

@dash.route('/events/contests/add/', methods=['GET'])
@login_required
# @staff_required("contests", 3)
def events_contest_add():

    print("GET Request for contest addition")
    mode = request.args.get('m')

    if mode is not None:
        if mode == "1":
            form = AddContest(request.form)
            return render_template('forms/dash/events/add_contests.html',
                                    form=form)
    else:
        return redirect(url_for('.events_show_contests', open=True))

    return jsonify(406)   

# Registrations

@dash.route('/registration/add/', methods=['GET', 'POST'])
@login_required
@staff_required("registration", 3)
def registration():
    
    form = AddRegistration(request.form)

    if request.method == 'POST':

        payload = {
            'vid': form.vid.data,
            'cat': form.cat.data,
            'eid': form.eid.data,
        }

        reg = requests.post(Config.HUB_URL+'/events/registration/staff', json=payload, headers={'Authorization':current_user.id})
        print("POSTED", reg)
        print("REPLY = ", reg.json().get('message'))  

        return jsonify(reg.json())

    return render_template('dash/registrations/registration_add.html', form=form)

@dash.route('/purchases/')
def purchases_home():
    saltotcount = requests.get(Config.HUB_URL+'/addons/order/stats', headers={'Authorization':current_user.id})
    purchases = requests.get(Config.HUB_URL+'/addons/order/staff', headers={'Authorization':current_user.id})
    print(saltotcount.json())
    print(purchases.json())
    return render_template('dash/regstats.html', stat=saltotcount.json(), purchases=purchases.json(), user=current_user)

@dash.route('/purchases/addons/buy/', methods=['GET', 'POST'])
@login_required
@staff_required("registration", 3)
def addons_staff():

    form = AddonVolunteer(request.form)

    if request.method == 'POST':

        payload = {
            'vid': form.vid.data,
            'pid': form.pid.data,
            'qty': form.qty.data,
            'roll': form.roll.data,
            'bookid': form.bookid.data, 
            'scount': form.scount.data,
            'mcount': form.mcount.data,
            'lcount': form.lcount.data,
            'xlcount': form.xlcount.data,
            'xxlcount': form.xxlcount.data
        }

        print("PAYLOAD = ", payload)

        reg = requests.post(Config.HUB_URL+'/addons/order/staff', json=payload, headers={'Authorization':current_user.id})
        print("REPLY = ", reg.json().get('message'))  

        return jsonify(reg.json())

    return render_template('dash/registrations/addons.html', form=form)


# Attendee dash beta

@dash.route('/')
@login_required
def dash_attendee():
    return render_template('dash/attendee_dash.html', user=current_user)