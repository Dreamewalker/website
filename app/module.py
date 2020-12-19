import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from app.database import db, User, Activity

def set_last_class_filter(index):
    if index % 2 == 0:
        return "last"
    else:
        return ""


bp = Blueprint('module', __name__)

bp.add_app_template_filter(set_last_class_filter, "set_last_class_filter")

@bp.route('/virtue', methods=['GET', 'POST'])
def virtue():
    if (request.method == 'GET'):
        act = Activity.query.filter(Activity.label == 'virtue').all()
        return render_template('Virtue.html', item=act)
        

@bp.route('/wisdom', methods=['GET', 'POST'])
def wisdom():
    if (request.method == 'GET'):
        act = Activity.query.filter(Activity.label == 'wisdom').all()
        return render_template('Wisdom.html', item=act)

@bp.route('/body', methods=['GET', 'POST'])
def body_act():
    if (request.method == 'GET'):
        act = Activity.query.filter(Activity.label == 'body').all()
        return render_template('Body.html', item=act)


@bp.route('/beauty', methods=['GET', 'POST'])
def beauty():
    if (request.method == 'GET'):
        act = Activity.query.filter(Activity.label == 'beauty').all()
        return render_template('Beauty.html', item=act)


@bp.route('/labor', methods=['GET', 'POST'])
def labor():
    if (request.method == 'GET'):
        act = Activity.query.filter(Activity.label == 'labor').all()
        return render_template('Labor.html', item=act)


@bp.route('/index', methods=['GET', 'POST'])
def index():
    act1 = None
    act2 = None
    act3 = None
    user = User.query.filter(User.id == g.userid).first()
    if user.usertype != 'student':
        return render_template('index.html', item1=act1, item2=act2, item3=act3)

    scores = {'virtue': 0, 'wisdom': 0, 'body': 0, 'beauty': 0, 'labor': 0}
    for activity in user.activities:
        if activity.status == 'finished' and activity.label in scores:
            scores[activity.label] += activity.score

    type1 = "virtue"  
    type2 = "wisdom"
    num1 = scores["virtue"]
    num2 = scores["wisdom"]
    for x,y in scores.items():
        if y < num1:
            type1 = x
        elif y < num2:
            type2 = x
    
    act1 = Activity.query.filter(Activity.label == type1 
            and user not in Activity.participants).first()
    act2 = Activity.query.filter(Activity.label == type1 
            and user not in Activity.participants
            and Activity.id != act1.id).first()
    act3 = Activity.query.filter(Activity.label == type2 
            and user not in Activity.participants).first()
    if act1 == None:
        act1 = Activity.query.filter(user not in Activity.participants).first()
    if act2 == None:
        act2 = Activity.query.filter(user not in Activity.participants
                and Activity.id != act1.id).first()
    if act3 == None:
        act3 = Activity.query.filter(user not in Activity.participants
                and Activity.id != act1.id 
                and Activity.id != act2.id).first()
    return render_template('index.html', item1=act1, item2=act2, item3=act3)
     