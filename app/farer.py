import requests
import datetime
from app import app, login
from flask import Blueprint, render_template, abort, redirect, request, url_for, jsonify
from jinja2 import TemplateNotFound
from config import Config
from app.models import User # College, FarerLog
from app.mail import farer_welcome_mail, amrsoy_reg_mail, testing_mail
from app.more import get_user_ip
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from flask_login import login_user, current_user, logout_user, login_required

farer = Blueprint('farer', __name__)

@login.user_loader
def load_user(id):

    print("Loading user")
    
    data = requests.get('http://localhost:3000/farer/auth/user', headers={'Authorization':id})
    staff = requests.get('http://localhost:3000/farer/staff', headers={'Authorization':id})
    
    print(data.json())
    print(staff.json())
    
    user = User(id=id, data=data.json().get('data'), staff=staff.json())
    
    print(id)
    print("End of loading user")
    
    return user

def f_login(request, point="None"):

    print("Inside authentication f_login")
    
    ip = get_user_ip(request)
    if current_user.is_authenticated:
        return jsonify(1)

    if request.method == 'POST':
        payload = {
            'idtoken': request.form['idtoken'],
            'user_ip': get_user_ip(request),
            'sender': 1
        }

        reply = requests.post('http://localhost:3000/farer/auth/user', json=payload)
        print(reply.json())

        return reply

# @farer.route('/login/')
# def login():
#     next_page = request.args.get('next')
#     if not next_page or url_parse(next_page).netloc != '':
#         next_page = url_for('index')
#     if (current_user.is_authenticated):
#         return "Welcome " + current_user.fname
#         if(current_user.datacomp == True_pa):
#             return redirect(url_for(nextge))
#         else:
#             return render_template('index.html', page="forms/details")
#     return render_template('accounts/login.html')

@farer.route('/logout/')
def logout():
    logout_user()
    print("Logging out user.")
    return "Logged out"

@farer.route('/user/')
@login_required
def user_print():
    print(current_user.id)
    print("Email:", current_user.data.get('email'))
    return "User"

@farer.route('/tokensignin/', methods=['GET','POST'])
# Send G-ID for sigin
def loggingIn():
    
    print("Intiating login")
    
    if current_user.is_authenticated:
        print("Authenticated")
        return "Already authenticated"
    
    if request.method == 'POST':
        print("PASSING TO F_LOGIN")
        reply_p = f_login(request).json()
        print(reply_p.json())

        reply_g = requests.get('http://localhost:3000/farer/auth/user', headers={'Authorization':reply_p.get('auth_token')})
        reply_g = reply_g.json()
        print("Reply-G", reply_g)
        print(reply_g.get('data'))

        u = User(id=reply_p.get('auth_token'), data=reply_g.get('data'))
        
        login_user(u, remember=True)
        
        return "Logged in"
    
    return "ERROR OCCURED DURING LOGIN"

@app.route('/data/farer/user/')
def farer_user():

    print("INISDE DATA FARER")
    print("USER = ", current_user.id)

    if current_user.is_authenticated:
        u = requests.get('http://localhost:3000/farer/auth/user', headers={'Authorization':current_user.id})
        print(u.json())
        return jsonify(u.json())

    return "false"
    
@farer.route('/details/')
@login_required
def farer_more():
    if current_user.detailscomp is True:
        return render_template('index.html', page = "/home")
    return render_template('index.html', page = "/forms/details")

@farer.route('/education/')
@login_required
def farer_education():
    print("DETAILS = " + str(current_user.detailscomp))
    print("EDU = " + str(current_user.educomp))
    if current_user.detailscomp is None:
        return render_template('index.html',
                                page = "/forms/details",
                                uchange="/farer/details/")
    if current_user.educomp is True:
        return render_template('index.html',
                                page = "/home",
                                uchange="")
    return render_template('index.html',
                            page = "/forms/education",
                            uchange="")
    # Rewrite to use the endpoints in Switch2 with contact to Hub

@farer.route('/delete/<id>/')
# @level_required(15)
def delete_user(id):
    u = User.query.filter_by(id=id).first()
    v = AmrSoyParticipant.query.filter_by(id=id).first()
    w = CAData.query.filter_by(id=id).first()
    flog = FarerLog(uid=u.id, action="Deletion")
    db.session.add(flog)
    if u is not None:
        db.session.delete(u)
    if u is not None:
        db.session.delete(v)
    if w is not None:
        db.session.delete(w)
    db.session.commit()
    return ('', 204)