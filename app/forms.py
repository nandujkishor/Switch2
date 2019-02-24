from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField, IntegerField, BooleanField, SubmitField, DateField, SelectField, DateTimeField, PasswordField
from wtforms.validators import DataRequired, ValidationError, InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class AddTalk(FlaskForm):
    permalink = StringField('permalink')
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    person = StringField('Person')
    # Take in a pic
    # picture = FileField('Picture', validators=[FileAllowed(['jpg', 'png'], 'JPG/PNG Image required')])
    # personpicsm = FileField('Person (small)', validators=[FileAllowed(['jpg', 'png'], 'JPG/PNG Image required')])
    # personpiclr = FileField('Person (large)', validators=[FileAllowed(['jpg', 'png'], 'JPG/PNG Image required')])
    amount = IntegerField('Amount')
    submit = SubmitField('Add Talk')


class AddWorkshop(FlaskForm):
    id = StringField('ID')
    wid = IntegerField('W-ID')
    title = StringField('Title', validators=[DataRequired()])
    department = StringField('Department')
    about = TextAreaField('Long description')
    short = TextAreaField('Short description')
    prereq = TextAreaField('Pre-requisites')
    rules = TextAreaField('Rules')
    # Take in a pic
    # picture1 = FileField('Picture 1', validators=[FileAllowed(['jpg', 'png'], 'JPG/PNG Image required')])
    # picture2 = FileField('Picture 2', validators=[FileAllowed(['jpg', 'png'], 'JPG/PNG Image required')])
    # picture3 = FileField('Picture 3', validators=[FileAllowed(['jpg', 'png'], 'JPG/PNG Image required')])
    org = StringField('Company Name')
    # complogo = FileField('Company Logo', validators=[FileAllowed(['jpg', 'png'], 'JPG/PNG Image required')])
    fee = IntegerField('Amount')
    support = IntegerField('V-ID of Incharge')
    seats = IntegerField('Number of slots')
    incharge = IntegerField('V-ID of Incharge')

class AddContest(FlaskForm):
    id = StringField('ID')
    cid = IntegerField('C-ID')
    title = StringField('Title', validators=[DataRequired()])
    plink = StringField('Permalink')
    short = TextAreaField('Short Description')
    about = TextAreaField('Description')
    prereq = TextAreaField('Pre-requisites')
    rules = TextAreaField('Rules')
    department = StringField('Department')
    prize1 = IntegerField('First prize')
    prize2 = IntegerField('Second prize')
    prize3 = IntegerField('Third prize')
    pworth = IntegerField('Third prize')
    team_limit = IntegerField('Team size limit')
    organiser = StringField('Organiser contact')
    contact = StringField('Organiser contact')
    fee = IntegerField('Amount')
    support = IntegerField('V-ID of Incharge')
    incharge = IntegerField('V-ID of Incharge')

def mobile_check(form, field):
    temp = str(field.data)
    if len(temp) != 10 or temp.isdigit() == False:
        raise ValidationError('Enter a valid mobile number')

class MoreData(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    sex = IntegerField('Gender', validators=[DataRequired()])
    phno = IntegerField('Mobile', validators=[mobile_check, DataRequired()])

class EduData(FlaskForm):
    course = StringField('Course', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    college = IntegerField('College', validators=[InputRequired()])
    institution = StringField('Institution')

class AmrSOY(FlaskForm):
    id = StringField('ID')
    house = IntegerField('House', validators=[DataRequired()])
    fear = StringField('What is your biggest Fear?', validators=[DataRequired()])

class CABegin(FlaskForm):
    id = StringField('ID')
    bio = TextAreaField('Short Introduction')

class CAQues(FlaskForm):
    id = StringField('ID')
    ans1 = TextAreaField('Answer 1', validators=[DataRequired()])
    ans2 = TextAreaField('Answer 2', validators=[DataRequired()])
    ans3 = TextAreaField('Answer 3', validators=[DataRequired()])
    ans4 = TextAreaField('Answer 4', validators=[DataRequired()])

class AmHackReg(FlaskForm):
    tsize = IntegerField('Tee size')
    # 1 for S, 2 for M, 3 for L, 4 for XL, 5 for XXL, 6 for XXXL
    github = StringField('Github profile')

class TeamCreate(FlaskForm):
    name = StringField('Team Name')

class AddTeamMember(FlaskForm):
    vid = IntegerField('VID 1')

class JudgePoints(FlaskForm):
    tid = IntegerField('Team ID')
    rev = IntegerField('Review')
    score = IntegerField('Score')

class HackSubmissionForm(FlaskForm):
    link = StringField('Github link')

class QAddQ1(FlaskForm):
    qtype = IntegerField('Question Type', validators=[DataRequired()])
    # Dropdown: Objective, Subjective
    qset = IntegerField('Question Set', validators=[DataRequired()])

class QAddQ2(FlaskForm):
    qid = IntegerField(validators=[DataRequired()])
    qtitle = TextAreaField('Question', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png'], 'JPG/PNG Image required')])
    qdesc = TextAreaField('Question Description')

class QAddObj(FlaskForm):
    qid = IntegerField(validators=[DataRequired()])
    pscore = IntegerField('Positive Score', validators=[DataRequired()])
    nscore = IntegerField('Negative Score', validators=[InputRequired()])
    op1 = StringField('Option 1', validators=[DataRequired()])
    op2 = StringField('Option 2', validators=[DataRequired()])
    op3 = StringField('Option 3 (Optional)')
    op4 = StringField('Option 4 (Optional)')
    op5 = StringField('Option 5 (Optional)')
    ans = IntegerField('Answer', validators=[DataRequired()])

class QAddSub(FlaskForm):
    qid = IntegerField()
    mscore = IntegerField('Maximum score')

class QAdd(FlaskForm):
    start = DateTimeField('Start Time', validators=[DataRequired()])
    end = DateTimeField('End Time', validators=[DataRequired()])
    passkey = PasswordField('Password', validators=[DataRequired()])

class QuizSubmission(FlaskForm):
    quid =  IntegerField('Quiz ID')
    qset = IntegerField('Quiz set')
    qid = IntegerField('Question ID')
    answer = StringField('Answer: Option ID or Desc. answer')
    time = DateTimeField('Time of Submission')

class PSS(FlaskForm):
    groups = [(1, 'Everyone'), (2, 'Details not completed'), (3, 'Education not completed'), (4, 'AMR SOY not completed')]
    group = SelectField('Group', choices=groups, validators=[DataRequired()])
    content = TextAreaField('Mail content', validators=[DataRequired()])
    check = BooleanField('Are you sure you know what this form does?')
    submit = SubmitField('Spam')

class test(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

class CreateStaff(FlaskForm):
    vid = IntegerField('VID of staff')
    team = StringField('Team of the staff')
    level = IntegerField('Level of the staff')

class AddRegistration(FlaskForm):
    vid = IntegerField('VID of staff')
    cat = IntegerField('Category of event')
    eid = IntegerField('Event ID')
