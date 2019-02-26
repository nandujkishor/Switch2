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
    data = request.form
    print(form.data, request.method)
    return ("Vidyut")