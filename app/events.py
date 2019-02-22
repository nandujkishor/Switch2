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

@events.route('/data/workshops/')
def workshops_listing():

    workshops = requests.get('http://localhost:3000/events/workshops')
    print(workshops.json())
    return jsonify(workshops.json())

@events.route('/data/contests/')
def contests_listing():

    contests = requests.get('http://localhost:3000/events/workshops')
    print(contests.json())
    return jsonify(contests.json())

@events.route('/data/workshops/<wtitle>', methods=['GET','POST','DELETE','PUT'])
def workshops_individual():

    print("Individual")
    return "Building"

