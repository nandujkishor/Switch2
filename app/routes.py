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


@app.route('/testing/')
def testing():
    return render_template('testing.html')


@app.route('/home', methods=['GET'])
def home():
    
    mode = request.args.get('m')
    print(mode)

    if mode is not None:
        if mode == "1":
            return render_template('home.html')
    else:
        return render_template('index.html', page="/home?m=1", uchange="")

@app.route('/talks/')
def talks():
    return render_template('coming.html')

@app.route('/concerts/')
def concert():
    return render_template('coming.html')

@app.route('/contests/')
def contests():
    return render_template('contests.html', page="contests-listing")

@app.route('/contests/<int:cid>/')
def contests_single(cid):
    mode = request.args.get('m')
    
    if mode is not None:
        if mode == "1":
            contest = Contests.query.filter_by(id=cid).first()
            if contest is None:
                return "404"
            
            support = User.query.filter_by(vid=contest.support).first()
            dept = ['CSE', 'ECE', 'ME', 'Physics', 'Chemisty', 'English', 'Biotech', 'BUG', 'Comm.', 'Civil', 'EEE', 'Gaming', 'Maths', 'Others']
            return render_template('individual-contests.html', page="contests-single", contest=contest, dept=dept, support=support)
    else:
        return render_template('contests.html', open=True,cid=cid)

@app.route('/workshops/')
def workshops():
    return render_template('workshops.html')

@app.route('/exhibitions/')
def exhibitions():
    return render_template('exhibitions.html')

@app.route('/sponsors/')
def sponsors():
    return render_template('sponsors.html')

@app.route('/workshops/<wtitle>/')
def workshop_single(wtitle):
    mode = request.args.get('m') 
    
    if mode is not None:
        if mode == "1":
            workshop = Workshops.query.filter_by(id=wtitle).first()
            support = User.query.filter_by(vid=workshop.support).first()
            if workshop is None:
                return "404"
            dept = ['CSE', 'ECE', 'ME', 'Physics', 'Chemisty', 'English', 'Biotech','BUG', 'Comm.', 'Civil', 'EEE', 'Gaming', 'Maths', 'Others']
            return render_template('individual-workshops.html', page="workshops-single", workshop = workshop, dept=dept, support=support)
    else:
        return render_template('workshops.html', open=True,wid=wtitle)

# forms

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
        print("REPLY FOR DETAILS ( PUT REQUEST ) ", reply.json())

        return jsonify(reply.json().get('status'))

    return render_template('forms/details.html', user=current_user, form=form)

@app.route('/forms/education/', methods=['GET', 'POST'])
@login_required
def forms_farer_edu():
    
    form = EduData(request.form)
    
    #colleges missing

    # colleges = requests.get('http://localhost:3000/farer/college/list')
    # colleges = colleges.json()

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

        reply = requests.put('http://localhost:3000/farer/user/education', json=payload, headers={'Authorization':current_user.id})
        
        print("REPLY FOR EDUCATION ( PUT REQUEST ) = ", reply.json())
        
        return jsonify(reply.json().get('status'))

    #Add colleges
    return render_template('forms/education.html', user=current_user, form=form)



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
