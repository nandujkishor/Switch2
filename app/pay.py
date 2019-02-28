import os, csv, json, datetime, requests
from app import app, login, mail
from flask import Blueprint, render_template, abort, redirect, request, url_for, jsonify
from jinja2 import TemplateNotFound
from config import Config
from app.models import User
from app.more import get_user_ip, access
from app.farer import staff_required
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from flask_login import login_user, current_user, logout_user, login_required

pay = Blueprint('pay', __name__)

@pay.route('/authorize', methods=['GET', 'POST'])
def payauth():
    try:
        if request.method == 'POST':
            payload = {
                'data':request.form.get('data'),
                # 'code':request.form.get('code')
            }
            r = requests.post(Config.HUB_URL+'/payments/receive', json=payload)
    except Exception as e:
        return "Exception occured : " + str(e)
    return ("Check localhost")

# @pay.route('/testing/', methods=['POST', 'GET'])
# def payment():
#     plaintext = "transactionId=VIDYUTTEST10|amount=1|purpose=VIDYUT19TEST|currency=inr"
#     result = hashlib.md5(plaintext.encode())
#     result = result.hexdigest()
#     print("md5",result)
#     pwc = plaintext + "|checkSum=" + result
#     print("before aes",pwc)
#     cipher = AESCipher(key)
#     encd = cipher.encrypt(pwc)
#     print("after aes", encd)
#     return encd

# @pay.route('/callback/', methods=['POST', 'GET'])
# def callback():
#     print("Inside callback")
#     print(request.args)
#     return "Check terminal"

@pay.route('/check/')
def check_pay():
    return render_template('payment.html')
