import os, csv, json, requests, datetime
from config import Config   
from flask import render_template, flash, redirect, request, url_for, jsonify
from app import app, login, mail
from app.models import User
from app.forms import AddTalk, AddWorkshop, MoreData, EduData, CreateStaff
from app.mail import farer_welcome_mail
from app.more import get_user_ip
from app.farer import staff_required
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from flask_login import login_user, current_user, logout_user, login_required

@login.unauthorized_handler
def unauthorized():
    return render_template('accounts/login.html', link="")

@app.route('/shit')
@login_required
def shit():
    r = requests.get(Config.HUB_URL + '/mail/test', headers={'Authorization':current_user.id})
    print(r.url)
    return "Hello"

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', page="/home?m=1", uchange="", user=current_user.is_authenticated)

@app.route('/home', methods=['GET'])
def home():
    mode = request.args.get('m')
    print(mode)

    if mode is not None:
        if mode == "1":
            return render_template('home.html', user=current_user.is_authenticated)
    else:
        return render_template('index.html', page="/home?m=1", uchange="", user=current_user.is_authenticated)

@app.route('/talks/')
def talks():
    return render_template('coming.html', user=current_user.is_authenticated)

@app.route('/concerts/')
def concert():
    return render_template('coming.html', user=current_user.is_authenticated)

@app.route('/exhibitions/')
def exhibitions():
    return render_template('exhibitions.html', user=current_user.is_authenticated)

@app.route('/contests/')
def contests():
    return render_template('contests.html', user=current_user.is_authenticated)

@app.route('/workshops/')
def workshops():
    return render_template('workshops.html', user=current_user.is_authenticated)

@app.route('/sponsors/')
def sponsors():
    return render_template('sponsors.html', user=current_user.is_authenticated)

# Individual pages

dept = ['CSE', 'ECE', 'ME', 'Physics', 'Chemisty', 'English', 'Biotech','BUG', 'Comm.', 'Civil', 'EEE', 'Gaming', 'Maths', 'Others']

@app.route('/workshops/<int:wid>/')
def workshop_single(wid):
    mode = request.args.get('m') 
    
    if mode is not None:
        if mode == "1":
            workshop = requests.get(Config.HUB_URL+'/events/workshops/'+str(wid))
            workshop = workshop.json()
            payload = {
                'vid': workshop.get('support')
            }
            support = requests.get(Config.HUB_URL+'/farer/user/contact', json=payload)
            support = support.json()
            if workshop is None:
                return "404"
            return render_template('individual-workshops.html', workshop = workshop, dept=dept, support=support)
    else:
        return render_template('workshops.html', open=True, wid=wid)

@app.route('/contests/<int:cid>/')
def contests_single(cid):
    mode = request.args.get('m')
    
    if mode is not None:
        if mode == "1":
            contest = requests.get(Config.HUB_URL+'/events/contests/'+str(cid))
            contest = contest.json()
            payload = {
                'vid': contest.get('support')
            }
            support = requests.get(Config.HUB_URL+'/farer/user/contact', json=payload)
            support = support.json()
            if contest is None:
                return "404"

            return render_template('individual-contests.html', contest=contest, dept=dept, support=support)
    else:
        return render_template('contests.html', open=True, cid=cid)

# Error handlers

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# URL services for Volunteers

@app.route('/staff/creation/', methods=['GET', 'POST'])
@staff_required(5)
def staff_creation():

    form = CreateStaff(request.form)

    if request.method == 'POST':

        payload = {
            'vid': form.vid.data,
            'team': form.team.data,
            'level': form.level.data
        }

        reply = requests.post(Config.HUB_URL + '/farer/staff', json=payload, headers={'Authorization':current_user.id})

        print(reply.json())
        return jsonify(reply.json().get('status'))

    return render_template('dash/staff_creation.html', form=form)

# import hashlib
# from Crypto.Cipher import AES
# import sys
# import base64
# from Crypto.Cipher import AES

# key = "WEGSNGOXHEUDEEDD" 
# iv = "3564234432724374"

# class AESCipher(object):
#     def __init__(self, key):
#         self.bs = 16
#         self.cipher = AES.new(key, AES.MODE_CBC, iv)

#     def encrypt(self, raw):
#         raw = self._pad(raw)
#         encrypted = self.cipher.encrypt(raw)
#         encoded = base64.b64encode(encrypted)
#         return str(encoded, 'utf-8')

#     def decrypt(self, raw):
#         decoded = base64.b64decode(raw)
#         decrypted = self.cipher.decrypt(decoded)
#         return str(self._unpad(decrypted), 'utf-8')

#     def _pad(self, s):
#         return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

#     def _unpad(self, s):
#         return s[:-ord(s[len(s)-1:])]

# @app.route('/payment/')
# def payment():
#     plaintext = "transactionId=HELLOWORLD|amount=1|purpose=VIDYUT19TEST|currency=inr"
#     result = hashlib.md5(plaintext.encode())
#     result = result.hexdigest()
#     print("md5",result)
#     pwc = plaintext + "|checkSum=" + result
#     print("before aes",pwc)
#     cipher = AESCipher(key)
#     encd = cipher.encrypt(pwc)
#     print("after aes", encd)
#     # URL = "https://payments.acrd.org.in/pay/makethirdpartypayment"
#     # PARAMS = {'encdata':encd,'code':"VIDYUT19TEST"}
#     return encd; 

@app.route('/check/')
def check_pay():
    return render_template('payment.html')