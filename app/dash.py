import os, csv, json, datetime, requests
from app import app, login, mail
from flask import Blueprint, render_template, abort, redirect, request, url_for, jsonify
from jinja2 import TemplateNotFound
from config import Config
from app.forms import AddTalk, AddWorkshop, AddContest, MoreData, CABegin, CAQues, test, EduData, AmrSOY
from app.models import User
from app.mail import farer_welcome_mail, amrsoy_reg_mail, testing_mail
from app.more import get_user_ip, access
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from flask_login import login_user, current_user, logout_user, login_required

dash = Blueprint('dash', __name__)

@dash.route('/lounge/')
@login_required
def lounge():
    users = requests.get('http://localhost:3000/farer/user/count', headers={'Authorization':current_user.id})
    users = users.json()
    colleges = requests.get('http://localhost:3000/farer/registered/college/count', headers={'Authorization':current_user.id})
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
    print(current_user)
    return render_template('dash/lounge.html',
                            user=current_user,
                            user_count=users.get('sub'),
                            colleges_count=colleges.get('sub'),
                            greeting=s,
                            notification=notification,
                            title="Switch Lounge")

@dash.route('/mc/maintenance/toggle/')
@login_required
# @level_required(20)
def mc_toggle_mtnc():
    Config.MAINTENANCE = not Config.MAINTENANCE
    return "Maintenance: " + Config.MAINTENANCE

@dash.route('/accounts/')
@login_required
# @level_required(8)
def accounts_home():

    user_arr = requests.get('http://localhost:3000/farer/user/list/short')
    user_arr = user_arr.json()

    return render_template('dash/accounts.html', users = user_arr,
                            user=current_user,
                            count = len(user_arr),
                            title="Accounts control")

@dash.route('/pss/', methods=['GET','POST'])
@login_required
# @level_required(20)
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
# @level_required(8)
def events_show_talks():
    
    return events_show(request.args.get('open'), "talks")

# Content to be pulled from the provided data endpoints

@dash.route('/events/workshops')
@login_required
# @level_required(8)
def events_show_workshops():

    return events_show(request.args.get('open'), "workshops")

@dash.route('/events/contests')
@login_required
# @level_required(8)
def events_show_contests():

    return events_show(request.args.get('open'), "contests")

@dash.route('/events/talks/add', methods=['GET'])
@login_required
# @level_required(8)
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
# @level_required(8)
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

# Data

# Data get

@dash.route('/data/get/events/talks/', methods=['GET'])
@login_required
# @level_required(8)
def events_talks():
    talks = requests.get('http://localhost:3000/events/talks', headers={'Authorization':current_user.id})
    talks = talks.json()
    return(talks)

@dash.route('/data/get/events/workshops/', methods=['GET'])
@login_required
# @level_required(8)
def events_workshops():
    workshops = requests.get('http://localhost:3000/events/workshops', headers={'Authorization':current_user.id})
    workshops = workshops.json()
    return(workshops)

@dash.route('/data/get/events/contests/', methods=['GET'])
@login_required
# @level_required(8)
def events_contests():
    contests = requests.get('http://localhost:3000/events/workshops', headers={'Authorization':current_user.id})
    contests = contests.json()
    return(contests)

#Data Post

@dash.route('/data/post/events/talks/', methods=['GET'])
@login_required
# @level_required(8)
def events_post_talks():
    
    form = AddTalk()

    if form.validate() == False:
        print(form.errors)
        return jsonify(form.errors)

    payload = {
        'title': form.title.data,
        'about': form.about.data,
        'person': form.person.data,
        'fee': form.amount.data,
        'incharge': form.incharge.data,
    }
   
    talks = requests.post('http://localhost:3000/events/talks', json=payload, headers={'Authorization':current_user.id})
    print(talks.get['message'])

    return jsonify(201)

@dash.route('/data/post/events/workshops/', methods=['GET'])
@login_required
# @level_required(8)
def events_post_workshops():

    form = AddWorkshop()

    if form.validate() == False:
        print(form.errors)
        return jsonify(form.errors)
    
    payload = {
        'title': form.title.data,
        'about': form.about.data,
        'short': form.short.data,
        'org': form.org.data,
        'fee': form.fee.data,
        'department': form.department.data,
        'incharge': form.incharge.data,
    }

    workshops = requests.post('http://localhost:3000/events/workshops', json=payload, headers={'Authorization':current_user.id})
    print(workshops.get['message'])

    return jsonify(201)

@dash.route('/data/post/events/contests/', methods=['GET'])
@login_required
# @level_required(8)
def events_post_contests():
    
    form = AddContest()

    if form.validate() == False:
        print(form.errors)
        return jsonify(form.errors)
    
    payload = {
        'title': form.title.data,
        'about': form.about.data,
        'short': form.short.data,
        'department': form.department.data,
        'prize1': form.prize1.data,
        'prize2': form.prize2.data,
        'prize3': form.prize3.data,
        'pworth': form.prize1.data,
        'team_limit': form.team_limit.data,
        'fee': form.fee.data,
        'incharge': form.incharge.data,
    }

    contests = requests.post('http://localhost:3000/events/contests', json=payload, headers={'Authorization':current_user.id})
    print(contests.get['message'])

    return jsonify(201)






