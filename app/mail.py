import smtplib
from config import Config
from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import render_template
from flask_login import current_user
# from app.models import User, FarerLog, AmHack, GoodieData, Team

def send_core(smtpserver, user, recipient, msg):
    smtpserver.sendmail(user, recipient, msg.as_string())
    smtpserver.close()

def send_mail(sub, body, htmlbody, recipient):
    smtpserver = smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = sub
    msg['From'] = Config.MAIL_DEFAULT_SENDER
    msg['To'] = recipient
    part1 = MIMEText(htmlbody, 'html')
    msg.attach(part1)

    Thread(target=send_core, args=(smtpserver, Config.MAIL_DEFAULT_SENDER, recipient, msg)).start()

def farer_welcome_mail():
    print("Inside the Welcome mail")
    send_mail("Thank you for registering with Vidyut", 
            body="Your Vidyut ID is " + str(current_user.vid), 
            htmlbody=render_template('emails/welcome.html', user=current_user), 
            recipient=current_user.email
            )
    return "Okay!"

def amrsoy_reg_mail():
    print("Inside AMRSoy mail")
    send_mail("Student of the Year 2019: Amrita Edition registration successful", 
            body="Thank you for your participation.", 
            htmlbody=render_template('emails/soy_welcome.html', user=current_user), 
            recipient=current_user.email
            )
    return "Okay!"

def testing_mail():
    print("Inside testing mail")
    send_mail("Testing mail",
            body="Thank you for your participation.",
            htmlbody=render_template('emails/soy_welcome.html', user=current_user),
            recipient=current_user.email
            )
    return "Mail sent"
