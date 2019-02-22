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
            'seats': form.seats.data,
            'rules': form.rules.data,
            'prereq': form.prereq.data,
            'support': form.support.data,
            'department': form.department.data,
            'incharge': form.incharge.data,
        }

        workshops = requests.post('http://localhost:3000/events/workshops', json=payload, headers={'Authorization':current_user.id})
        print(workshops.json().get('message'))  

        return jsonify(201)

    workshops = requests.get('http://localhost:3000/events/workshops')
    print(workshops.json())
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
            'pworth': form.prize1.data + form.prize2.data + form.prize3.data,
            'team_limit': form.team_limit.data,
            'fee': form.fee.data,
            'incharge': form.incharge.data,
            'rules': form.rules.data,
            'prereq': form.prereq.data,
            'support': form.support.data
        }

        contests = requests.post('http://localhost:3000/events/contests', json=payload, headers={'Authorization':current_user.id})
        
        print(contests.json().get('message'))

        return jsonify(201)

    contests = requests.get('http://localhost:3000/events/contests')
    print(contests.json())
    return jsonify(contests.json())

@events.route('/data/workshops/<int:id>/', methods=['GET','DELETE','PUT'])
def workshops_individual(id):

    if request.method == 'DELETE':
        delete_reply = requests.delete('http://localhost:3000/events/workshops/'+str(id), headers={'Authorization':current_user.id})
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
            'seats': form.seats.data,
            'rules': form.rules.data,
            'prereq': form.prereq.data,
            'support': form.support.data,
            'department': form.department.data,
            'incharge': form.incharge.data,
        }

        workshops = requests.put('http://localhost:3000/events/workshops/'+str(id), json=payload, headers={'Authorization':current_user.id})

        print(workshops.json().get('message'))  

        return jsonify(workshops.json().get('message'))

    workshop = requests.get('http://localhost:3000/events/workshops/'+str(id))
    print(workshop.json())
    return jsonify(workshop.json())

@events.route('/data/contests/<int:id>/', methods=['GET','DELETE','PUT'])
def contests_individual(id):

    if request.method == 'DELETE':
        delete_reply = requests.delete('http://localhost:3000/events/contests/'+str(id), headers={'Authorization':current_user.id})
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
            'team_limit': form.team_limit.data,
            'fee': form.fee.data,
            'incharge': form.incharge.data,
            'rules': form.rules.data,
            'prereq': form.prereq.data,
        }

        contests = requests.put('http://localhost:3000/events/contests/'+str(id), json=payload, headers={'Authorization':current_user.id})
        
        print(contests.json().get('status'))

        return jsonify(contests.json().get('status'))

    contest = requests.get('http://localhost:3000/events/contests/'+str(id))
    print(contest.json())
    return jsonify(contest.json())
