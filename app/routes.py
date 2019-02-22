import os, csv, json, requests, datetime
from config import Config
from flask import render_template, flash, redirect, request, url_for, jsonify
from app import app, login, mail
from app.models import User
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

@app.route('/exhibitions/')
def exhibitions():
    return render_template('exhibitions.html')

@app.route('/contests/')
def contests():
    return render_template('contests.html')

@app.route('/workshops/')
def workshops():
    return render_template('workshops.html')

@app.route('/sponsors/')
def sponsors():
    return render_template('sponsors.html')

# Individual pages

dept = ['CSE', 'ECE', 'ME', 'Physics', 'Chemisty', 'English', 'Biotech','BUG', 'Comm.', 'Civil', 'EEE', 'Gaming', 'Maths', 'Others']

@app.route('/workshops/<wtitle>/')
def workshop_single(wtitle):
    mode = request.args.get('m') 
    
    if mode is not None:
        if mode == "1":
            workshop = requests.get('http://localhost:3000/events/workshop/'+str(wtitle))
            support = User.query.filter_by(vid=workshop.support).first()
            if workshop is None:
                return "404"
            return render_template('individual-workshops.html', page="workshops-single", workshop = workshop, dept=dept, support=support)
    else:
        return render_template('workshops.html', open=True,wid=wtitle)

@app.route('/contests/<int:cid>/')
def contests_single(cid):
    mode = request.args.get('m')
    
    if mode is not None:
        if mode == "1":
            contest = Contests.query.filter_by(id=cid).first()
            if contest is None:
                return "404"
            
            support = User.query.filter_by(vid=contest.support).first()
            return render_template('individual-contests.html', page="contests-single", contest=contest, dept=dept, support=support)
    else:
        return render_template('contests.html', open=True,cid=cid)

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
