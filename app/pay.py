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

import hashlib
from Crypto.Cipher import AES
import sys
import base64
from Crypto.Cipher import AES

key = "WEGSNGOXHEUDEEDD" 
iv = "3564234432724374"

pay = Blueprint('pay', __name__)

class AESCipher(object):
    def __init__(self, key):
        self.bs = 16
        self.cipher = AES.new(key, AES.MODE_CBC, iv)

    def encrypt(self, raw):
        raw = self._pad(raw)
        encrypted = self.cipher.encrypt(raw)
        encoded = base64.b64encode(encrypted)
        return str(encoded, 'utf-8')

    def decrypt(self, raw):
        decoded = base64.b64decode(raw)
        decrypted = self.cipher.decrypt(decoded)
        return str(self._unpad(decrypted), 'utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

@pay.route('/authorize/', methods=['GET', 'POST'])
def payauth():
    payload = {
        'code': request.form.get('code'),
        'data': request.form.get('data')
    }
    r = requests.post('http://localhost:5000/pay/callback/', json=payload)

    return ("Check localhost")

@pay.route('/testing/', methods=['POST'])
def payment():	
    i = request.form.get('id')
    print(i)
    tid = "transactionId=VIDYUTTEST" + str(i)
    plaintext = tid + "|amount=1|purpose=VIDYUT19TEST|currency=inr"
    result = hashlib.md5(plaintext.encode())
    result = result.hexdigest()
    print("md5",result)
    pwc = plaintext + "|checkSum=" + result
    print("before aes",pwc)
    cipher = AESCipher(key)
    encd = cipher.encrypt(pwc)
    print("after aes", encd)
    return encd

@pay.route('/callback/', methods=['POST', 'GET'])
def callback():
    print(request.get_json())
    return "Check terminal"

@pay.route('/check/')
def check_pay():
    return render_template('payment.html')