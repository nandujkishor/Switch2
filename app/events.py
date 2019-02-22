import datetime
from app import app, login
from flask import Blueprint, render_template, abort, redirect, request, url_for, jsonify
from jinja2 import TemplateNotFound
from config import Config
from google.oauth2 import id_token
from google.auth.transport import requests
from app.models import User
from app.forms import AddWorkshop, AddContest, AddTalk, EduData, MoreData
from app.more import  get_user_ip
from app.farer import f_login
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from flask_login import current_user, login_required

events = Blueprint('events', __name__)

# @aevents.route('/talks/')
# class events_talks(Resource):
#     @api.doc('List of all talks')
#     def get(self):
#         talks = Talks.query.all()
#         return jsonify(Talks.serialize_list(talks))
    
#     @login_required
#     @api.doc('Talk addition - need level 8 access')
#     def post(self):
        
#         form = AddTalk()

#         if form.validate() == False:
#             print(form.errors)
#             return jsonify(form.errors)

#         # f1 = form.picture.data
#         # f2 = form.personpicsm.data
#         # f3 = form.personpiclr.data
#     	# ext = os.path.splitext(filename)[1]
#         talk = Talks(title=form.title.data,
#                     descr=form.description.data,
#                     person=form.person.data,
#                     amt=form.amount.data
#                     )
#         db.session.add(talk)
#         db.session.commit()
#         # talk.picurl = 
#         # f1l = os.path.join(app.instance_path, 'images', )
#         # f2l = os.path.join(app.instance_path, 'images', secure_filename(f2.filename))
#         # f3l = os.path.join(app.instance_path, 'images', secure_filename(f3.filename))
#         # Need to put these into S3 using the APIs
#         # f1.save(f1l)
#         # f2.save(f2l)
#         # f3.save(f3l)
#         print(talk)
#         return jsonify(201)

# @aevents.route('/talks/<int:id>/')
# class events_talks_indv(Resource):
#     def get(self, id):
#         talk = Talks.query.filter_by(id=id).first()
#         return jsonify(talk.serialize())
    
#     @login_required
#     def put(self, id):
#         talk = Talks.query.filter_by(id=id).first()
#         return "Too lame to finish."

#     @login_required
#     def delete(self, id):

#         talk = Talks.query.filter_by(id=id).first()
        
#         if talk is not None:
#             db.session.delete(talk)
#             db.session.commit()
#             return jsonify(200)
        
#         return jsonify(406)


# @aevents.route('/workshops/')
# class events_workshops(Resource):
#     def get(self):
#         # if current_user.is_authenticated and (current_user.level >= 8 or current_user.super()):
#         workshops = Workshops.query.all()
#         # else:
#         #     workshops = Workshops.query.filter_by(pub=True).all()
#         return jsonify(Workshops.serialize_list(workshops))
    
#     @login_required
#     def post(self):
#         form = AddWorkshop()
#         print(form.data)

#         # if form.validate() == False:
#         #     print(form.errors)
#         #     return jsonify(form.errors)
        
#         workshop = Workshops(title=form.title.data,
#                     short=form.short.data,
#                     about=form.about.data,
#                     org=form.org.data,
#                     fee=form.fee.data,
#                     incharge=form.incharge.data,
#                     support=form.support.data,
#                     prereq=form.prereq.data,
#                     rules=form.rules.data,
#                     department = form.department.data,
#                     seats = form.seats.data,
#                     )
#         db.session.add(workshop)
#         db.session.commit()
#         return jsonify(201)

#     @login_required
#     def put(self):
#         form = AddWorkshop()
#         print(form.data)

#         # if form.validate() == False:
#         #     print(form.errors)
#         #     return jsonify(form.errors)
        
#         workshop = Workshops.query.filter_by(id=form.wid.data).first()
#         print(workshop)
#         if workshop is None:
#             return jsonify(401)
#         workshop.title = form.title.data
#         workshop.short = form.short.data
#         workshop.about = form.about.data
#         workshop.org = form.org.data
#         workshop.fee = form.fee.data
#         workshop.incharge=form.incharge.data
#         workshop.support=form.support.data
#         workshop.prereq=form.prereq.data
#         workshop.rules=form.rules.data
#         workshop.department = form.department.data
#         workshop.seats = form.seats.data
#         db.session.commit()
#         return jsonify(201)

# @aevents.route('/contests/')
# class events_workshops(Resource):
#     def get(self):
#         contests = Contests.query.all()
#         return jsonify(Contests.serialize_list(contests))
    
#     @login_required
#     def post(self):
#         form = AddContest()

#         # if form.validate() == False:
#         #     print(form.errors)
#         #     return jsonify(form.errors)
        
#         contest = Contests(title=form.title.data,
#                     about=form.about.data,
#                     short=form.short.data,
#                     fee=form.fee.data,
#                     prize1=form.prize1.data,
#                     prize2=form.prize2.data,
#                     prize3=form.prize3.data,
#                     pworth= form.prize1.data+form.prize2.data+form.prize3.data,
#                     incharge=form.incharge.data,
#                     support=form.support.data,
#                     prereq=form.prereq.data,
#                     rules=form.rules.data,
#                     team_limit=form.team_limit.data,
#                     department = form.department.data,
#                     )
#         db.session.add(contest)
#         db.session.commit()
#         return jsonify(201)

#     @login_required
#     def put(self):
#         form = AddContest()

#         # if form.validate() == False:
#         #     print(form.errors)
#         #     return jsonify(form.errors)
        
#         contest = Contests.query.filter_by(id=form.cid.data).first()

#         if contest is None:
#             return jsonify(401)
#         print(form.short.data)
#         contest.title=form.title.data
#         contest.about=form.about.data
#         contest.short=form.short.data
#         contest.fee=form.fee.data
#         contest.prize1=form.prize1.data
#         contest.prize2=form.prize2.data
#         contest.prize3=form.prize3.data
#         contest.pworth= form.prize1.data+form.prize2.data+form.prize3.data
#         contest.incharge=form.incharge.data
#         contest.support=form.support.data
#         contest.prereq=form.prereq.data
#         contest.rules=form.rules.data
#         contest.team_limit=form.team_limit.data
#         contest.department = form.department.data
#         db.session.commit()
#         return jsonify(201)

# @aevents.route('/workshops/<int:id>/')
# class events_workshops_indv(Resource):
#     def get(self, id):
#         workshop = Workshops.query.filter_by(id=id).first()
#         return jsonify(workshop.serialize())
    
#     @login_required
#     def put(self, id):
#         workshop = Workshops.query.filter_by(id=id).first()
#         return "Too lame to finish."

#     @login_required
#     def delete(self, id):

#         workshop = Workshops.query.filter_by(id=id).first()
        
#         if workshop is not None:
#             db.session.delete(workshop)
#             db.session.commit()
#             return jsonify(200)
        
#         return jsonify(406)

# @aevents.route('/contests/<int:id>/')
# class events_contests_indv(Resource):
#     def get(self, id):
#         contest = Contests.query.filter_by(id=id).first()
#         return jsonify(contest.serialize())
    
#     @login_required
#     def put(self, id):
#         contest = Contests.query.filter_by(id=id).first()
#         return "Too lame to finish."

#     @login_required
#     def delete(self, id):

#         contest = Contests.query.filter_by(id=id).first()
        
#         if contest is not None:
#             db.session.delete(contest)
#             db.session.commit()
#             return jsonify(200)
        
#         return jsonify(406)