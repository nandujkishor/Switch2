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
    notification = "No notifications."
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
# @staff_required(4)
def accounts_home():

    user_arr = requests.get(Config.HUB_URL+'/farer/user/list/short', headers={'Authorization':current_user.id})
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


@dash.route('/events/talks')
@login_required
@staff_required("all", 4)
def events_show_talks():

    return events_show(request.args.get('open'), "talks")

# Content to be pulled from the provided data endpoints
@dash.route('/events/')
@dash.route('/events/workshops')
@login_required
@staff_required("all", 4)
def events_show_workshops():

    return events_show(request.args.get('open'), "workshops")

@dash.route('/events/contests')
@login_required
@staff_required("all", 4)
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
@staff_required("all", 4)
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
@staff_required("all", 4)
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
@login_required
@staff_required("all", 4)
def purchases_home():
    saltotcount = requests.get(Config.HUB_URL+'/addons/order/stats', headers={'Authorization':current_user.id})
    purchases = requests.get(Config.HUB_URL+'/addons/order/staff', headers={'Authorization':current_user.id})
    return render_template('dash/regstats.html', stat=saltotcount.json(), purchases=purchases.json(), user=current_user)

@dash.route('/registrations/')
@login_required
@staff_required("all", 4)
def registrations_home():
    registrations = requests.get(Config.HUB_URL+'/events/registration/all', headers={'Authorization':current_user.id})
    stat = requests.get(Config.HUB_URL+'/events/registration/stats', headers={'Authorization':current_user.id})
    return render_template('dash/regevtstats.html', registrations=registrations.json(), stat=stat.json(), user=current_user)

@dash.route('/registrations/events/')
@login_required
@staff_required("all", 4)
def event_registrations_data():
    try:
        data1 = requests.get(Config.HUB_URL+'/events/registration/count', headers={'Authorization':current_user.id})
    except Exception as e:
        print(e)
        return "Error occured: "+str(e)
    teventsdata = data1.json()
    wdata = teventsdata.get('wdata')
    cdata = teventsdata.get('cdata')
    wamt = teventsdata.get('wamt')
    camt = teventsdata.get('camt')
    return render_template('dash/regevents.html', wdata=wdata, cdata=cdata, user=current_user, wamt=wamt, camt=camt)

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

    return redirect(url_for('routes.page_not_found'))

@dash.route('/purchases/addons/buy/amr/')
@login_required
@staff_required("registration", 3)
def addons_staff_amr():

    form = AddonVolunteer(request.form)
    return render_template('dash/registrations/addons_amr.html', form=form)

@dash.route('/purchases/addons/buy/out/')
@login_required
@staff_required("registration", 3)
def addons_staff_out():

    form = AddonVolunteer(request.form)
    return render_template('dash/registrations/addons_out.html', form=form)

# Attendee dash beta

@dash.route('/')
@login_required
def dash_attendee():
    purchases = requests.get(Config.HUB_URL+'/addons/order/my', headers={'Authorization':current_user.id})
    workshops = requests.get(Config.HUB_URL+'/events/registration/workshops', headers={'Authorization':current_user.id})
    contests = requests.get(Config.HUB_URL+'/events/registration/contests', headers={'Authorization':current_user.id})
    return render_template('dash/attendee_dash.html', purchases=purchases.json(),user=current_user, workshops=workshops.json(), contests=contests.json())

@dash.route('/delivery')
@login_required
# @staff_required("registration", 3)
def delivery():
    return render_template('dash/registrations/delivery.html')

@dash.route('/delivery/data/<int:vid>', methods=['GET', 'POST'])
@login_required
def delivery_data(vid):
    
    if request.method == 'POST':
        r = requests.post(Config.HUB_URL+'/addons/deliver/'+str(vid), headers={'Authorization':current_user.id})
        print(r.json().get('status'))
        return jsonify(r.json().get('status'))

    r = requests.get(Config.HUB_URL+'/addons/deliver/'+str(vid), headers={'Authorization':current_user.id})
    print(r.json())
    return(jsonify(r.json()))

@dash.route('/delivery/shirt/<int:vid>', methods=['POST'])
@login_required
def delivery_shirt(vid):
    data = request.get_json()
    payload = {
        'purid': request.form.get('purid')
    }
    r = requests.post(Config.HUB_URL+'/addons/deliver/shirt/'+str(vid), json=payload, headers={'Authorization':current_user.id})
    print(r.json().get('status'))
    return jsonify(r.json())

@dash.route('/delivery/ticket/<int:vid>', methods=['POST'])
@login_required
def delivery_ticket(vid):

    payload = {
        'purid': request.form.get('purid')
    }

    r = requests.post(Config.HUB_URL+'/addons/deliver/ticket/'+str(vid),json=payload, headers={'Authorization':current_user.id})
    print(r.json().get('status'))
    return jsonify(r.json())

@dash.route('/delivery/all/<int:vid>', methods=['POST'])
@login_required
def delivery_all(vid):

    payload = {
        'purid': request.form.get('purid')
    }

    r = requests.post(Config.HUB_URL+'/addons/deliver/'+str(vid),json=payload, headers={'Authorization':current_user.id})
    print(r.json().get('status'))
    return jsonify(r.json())