import os
import csv
import json
import requests
import datetime
from flask import render_template, flash, redirect, request, url_for, jsonify
from app import app, login, mail
from app.models import User
from config import Config
from app.forms import AddTalk, AddWorkshop, MoreData, CABegin, CAQues, test, EduData, AmrSOY
from app.mail import farer_welcome_mail, amrsoy_reg_mail, testing_mail
from app.more import get_user_ip
from app.farer import Auth
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from flask_login import login_user, current_user, logout_user, login_required

@login.unauthorized_handler
def unauthorized():
    return render_template('accounts/login.html', link="")

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', page="/home?m=1", uchange="")

@app.route('/home', methods=['GET'])
def home():
    
    mode = request.args.get('m')
    print(mode)

    if mode is not None:
        if mode == "1":
            return render_template('home.html')
    else:
        return render_template('index.html', page="/home?m=1", uchange="")

@app.route('/tests/ip/')
def tests_ip():
    return jsonify(get_user_ip(request))

@app.route('/workshops/')
def workshops():
    return render_template('workshops.html')

@app.route('/workshops/individual', methods=['GET'])
def workshop_single():
    return render_template('individual.html');

def workshops():
    return render_template('workshops.html', page="workshops-single")

@app.route('/forms/details/', methods=['GET', 'POST'])
@login_required
# Time to migrate to APIs
def forms_farer_more():
    form = MoreData(request.form)

    if request.method == 'POST':

        print("Validation = " + str(form.validate()))
        if form.validate() == False:
            print(form.errors)
            return jsonify(form.errors)
        
        payload = {
            'fname': form.fname.data,
            'lname': form.lname.data,
            'phno': form.phno.data,
            'sex': form.sex.data,
            'detailscomp': True
        }

        reply = requests.put('http://localhost:3000/farer/user/details', json=payload,  headers={'Authorization':current_user.id})
        print(reply.json())
        return jsonify(reply.json())

    return render_template('forms/details.html', user=current_user, form=form)

@app.route('/forms/education/', methods=['GET', 'POST'])
@login_required
def forms_farer_edu():
    form = EduData(request.form)
    colleges = requests.get('http://localhost:3000/farer/college/list')
    colleges = colleges.json()

    if request.method == 'POST':

        print("Validation = " + str(form.validate()))

        if form.validate() == False:
            print(form.errors)
            return jsonify(form.errors)

        payload = {
            'course': form.course.data,
            'major': form.major.data,
            'college': form.college.data,
            'institution': form.institution.data,
            'year': form.year.data,
            'educomp': True
        }

        reply = requests.post('http://localhost:3000/farer/user/education', json=payload, headers={'Authorization':current_user.id})
        print(reply.get['message'])
        
    return render_template('forms/education.html', user=current_user, colleges=colleges, form=form)

# Error handlers

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# URL services for Volunteers

@app.route('/staff/login/')
def volunteers_accounts_login():
    if (current_user.is_authenticated):
        return redirect('/dash/lounge/')
    return render_template('accounts/login.html', link='/dash/lounge')
