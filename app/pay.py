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
            r = requests.post(Config.HUB_URL+'/pay/receive', json=payload)
            return ("POSTED TO " + str(r.json()))
    except Exception as e:
        return "Exception occured : " + str(e)
    return ("Check localhost")

@pay.route('/check/')
def check_pay():
    return render_template('payment.html')

@pay.route('/probe')
def payprobe():
    return render_template('probe.html')
@pay.route('/addon', methods=['GET', 'POST'])
@login_required
def addon_pay():
    try:
        pid = request.form['pid']
        qty = request.form['qty']
        payload = {
            'pid': int(pid),
            'qty': int(qty)
        }
        print(payload)
        r = requests.post(Config.HUB_URL+'/addons/order/new', json=payload, headers={'Authorization':current_user.id})
    except Exception as e:
        print(e)
        responseObject = {
            'status':'fail',
            'message':'Internal server communication Issue (Error:'+str(e)
        }
        return jsonify(responseObject)
    return jsonify(r.json())