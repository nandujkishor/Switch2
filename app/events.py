import datetime, requests
from app import app, login
from flask import Blueprint, render_template, abort, redirect, request, url_for, jsonify
from jinja2 import TemplateNotFound
from config import Config
from app.models import User
from app.forms import AddWorkshop, AddContest, AddTalk, EduData, MoreData
from app.more import  get_user_ip
from app.farer import f_login
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from flask_login import current_user, login_required

events = Blueprint('events', __name__)

@events.route('/data/workshops/', methods=['GET', 'POST'])
def workshops_listing():
    if request.method == 'POST' or request.method == 'PUT':
        form = AddWorkshop(request.form)

        payload = {
            'title': form.title.data,
            'about': form.about.data,
            'short': form.short.data,
            'org': form.org.data,
            'fee': form.fee.data,
            'venue': form.venue.data,
            'seats': form.seats.data,
            'rules': form.rules.data,
            'prereq': form.prereq.data,
            'd1dur': form.d1dur.data,
            'd2dur': form.d2dur.data,
            'd3dur': form.d3dur.data,
            'support': form.support.data,
            'department': form.department.data,
            'incharge': form.incharge.data,
        }

        workshops = requests.post(Config.HUB_URL+'/events/workshops', json=payload, headers={'Authorization':current_user.id})
        print(workshops.json().get('message'))  

        return jsonify(201)

    workshops = requests.get(Config.HUB_URL+'/events/workshops')
    # print(workshops.json())
    return jsonify(workshops.json())

@events.route('/data/contests/', methods=['GET', 'POST', 'DELETE'])
def contests_listing():
    if request.method == 'POST' or request.method == 'PUT':
        form = AddContest(request.form)
        
        payload = {
            'title': form.title.data,
            'about': form.about.data,
            'short': form.short.data,
            'department': form.department.data,
            'prize1': form.prize1.data,
            'prize2': form.prize2.data,
            'prize3': form.prize3.data,
            'd1dur': form.d1dur.data,
            'venue': form.venue.data,
            'd2dur': form.d2dur.data,
            'd3dur': form.d3dur.data,
            'pworth': form.prize1.data + form.prize2.data + form.prize3.data,
            'team_limit': form.team_limit.data,
            'fee': form.fee.data,
            'incharge': form.incharge.data,
            'rules': form.rules.data,
            'prereq': form.prereq.data,
            'support': form.support.data
        }

        contests = requests.post(Config.HUB_URL+'/events/contests', json=payload, headers={'Authorization':current_user.id})
        
        print(contests.json().get('message'))

        return jsonify(201)

    contests = requests.get(Config.HUB_URL+'/events/contests')
    # print(contests.json())
    return jsonify(contests.json())

@events.route('/data/workshops/<int:id>/', methods=['GET','DELETE','PUT'])
def workshops_individual(id):

    if request.method == 'DELETE':
        delete_reply = requests.delete(Config.HUB_URL+'/events/workshops/'+str(id), headers={'Authorization':current_user.id})
        print(delete_reply.json())

        return jsonify(201)
    
    if request.method == 'PUT':
        form = AddWorkshop(request.form)

        payload = {
            'title': form.title.data,
            'about': form.about.data,
            'short': form.short.data,
            'org': form.org.data,
            'fee': form.fee.data,
            'venue': form.venue.data,
            'seats': form.seats.data,
            'rules': form.rules.data,
            'd1dur': form.d1dur.data,
            'd2dur': form.d2dur.data,
            'd3dur': form.d3dur.data,
            'prereq': form.prereq.data,
            'support': form.support.data,
            'department': form.department.data,
            'incharge': form.incharge.data,
        }

        workshops = requests.put(Config.HUB_URL+'/events/workshops/'+str(id), json=payload, headers={'Authorization':current_user.id})

        print(workshops.json().get('message'))  

        return jsonify(workshops.json().get('message'))

    workshop = requests.get(Config.HUB_URL+'/events/workshops/'+str(id))
    print(workshop.json())
    return jsonify(workshop.json())

@events.route('/data/contests/<int:id>/', methods=['GET','DELETE','PUT'])
def contests_individual(id):

    if request.method == 'DELETE':
        delete_reply = requests.delete(Config.HUB_URL+'/events/contests/'+str(id), headers={'Authorization':current_user.id})
        print(delete_reply.json())

        return jsonify(201)
    
    if request.method == 'PUT':
        form = AddContest(request.form)
        
        payload = {
            'title': form.title.data,
            'about': form.about.data,
            'short': form.short.data,
            'department': form.department.data,
            'prize1': form.prize1.data,
            'prize2': form.prize2.data,
            'prize3': form.prize3.data,
            'pworth': form.prize1.data,
            'd1dur': form.d1dur.data,
            'd2dur': form.d2dur.data,
            'd3dur': form.d3dur.data,
            'venue': form.venue.data,
            'team_limit': form.team_limit.data,
            'fee': form.fee.data,
            'support': form.support.data,
            'incharge': form.incharge.data,
            'rules': form.rules.data,
            'prereq': form.prereq.data,
        }

        contests = requests.put(Config.HUB_URL+'/events/contests/'+str(id), json=payload, headers={'Authorization':current_user.id})
        
        print(contests.json().get('status'))

        return jsonify(contests.json().get('status'))

    contest = requests.get(Config.HUB_URL+'/events/contests/'+str(id))
    print(contest.json())
    return jsonify(contest.json())

@events.route('/register', methods=['GET', 'POST'])
def events_register():

    if request.method == 'POST':
        payload = {
            'cat': 1,
            'eid': 62,
        }
        req = requests.post(Config.HUB_URL+'/events/registration', json=payload, headers={'Authorization':current_user.id})
        print(req.json())

        return jsonify(req.json())

    return render_template('payment.html')

@events.route('/data/registered/', methods=['GET'])
def events_registered():

    events = requests.get(Config.HUB_URL+'/events/registration', headers={'Authorization':current_user.id})    
    print(events)

    return jsonify(events.json())