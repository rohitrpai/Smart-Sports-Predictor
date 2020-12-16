import re
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime
import numpy as np
from tensorflow import keras
import os

app_with_orm = Flask(__name__)
Bootstrap(app_with_orm)
app_with_orm.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app_with_orm.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app_with_orm)


class users(db.Model):
   __tablename__ = 'users'
   user_id = Column(Integer, primary_key=True, autoincrement=True)
   first_name = Column(String, nullable=False)
   last_name = Column(String)
   user_name = Column(String)
   password = Column(String)
   email_id = Column(String)
   created_at = Column(DateTime, default=datetime.utcnow)


class dashboard(db.Model):
    __tablename__ = 'dashboard'
    dashboard_id = Column(Integer, primary_key=True)
    email_id = Column(String, nullable=False)
    matches_played = Column(Integer)
    runs_scored = Column(Integer)
    wicket_taken = Column(Integer)


def __init__(self, first_name, last_name, user_name, password, email_id):
   self.first_name = first_name
   self.last_name = last_name
   self.user_name = user_name
   self.password = password
   self.email_id = email_id


@app_with_orm.route('/')
@app_with_orm.route('/main', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        uname = session.get("username", "Unknown")
        if uname == "Unknown":
            return render_template('main.html')
        else:
            return redirect(url_for("home"))


@app_with_orm.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    status = 200
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            msg = 'Please enter your username/password!'
            status = 401
            return render_template('login.html', msg=msg), status
        account = users.query.filter_by(user_name=username, password=password).first()
        if account:
            fname = account.first_name if hasattr(account, 'first_name') else None
            email = account.email_id if hasattr(account, 'email_id') else None
            session['loggedin'] = True
            # session['id'] = account['id']
            session['username'] = username
            session['fname'] = fname
            session['email_id'] = email
            msg = 'Logged in successfully !'
            return redirect(url_for("home"))
        else:
            msg = 'Incorrect username / password !'
            status= 401
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
        status = 401
    elif request.method == 'GET':
        uname = session.get("username", "Unknown")
        if uname == "Unknown":
            return render_template('login.html')
        else:
            return redirect(url_for("home"))
    return render_template('login.html', msg=msg), status


@app_with_orm.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app_with_orm.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account = users.query.filter_by(user_name = username).first()
        if account:
            msg = 'Account already exists !'
        elif not firstname or not lastname or not username or not password or not email:
            msg = 'Please fill out the form !'
        elif not re.match(r'[A-Za-z]', firstname):
            msg = 'First Name must contain only alphabets!'
        elif not re.match(r'[A-Za-z]', lastname):
            msg = 'Last Name must contain only alphabets!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        else:
            user = users(first_name= firstname, last_name = lastname, user_name = username, password = password, email_id = email)
            db.session.add(user)
            db.session.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    elif request.method == 'GET':
        uname = session.get("username", "Unknown")
        if uname == "Unknown":
            return render_template('registration.html')
        else:
            return redirect(url_for("home"))
    return render_template('registration.html', msg=msg)


@app_with_orm.route('/home', methods=['GET', 'POST'])
def home():
    msg = ''
    if request.method == 'GET':
        uname = session.get("username", "Unknown")
        if uname == "Unknown":
            return redirect(url_for('login'))
        else:
            details = dashboard.query.filter_by(email_id=session['email_id']).first()
            if details == None:
                msg2 = '0'
                msg3 = '0'
                msg4 = '0'
            else:
                msg2 = str(details.matches_played if hasattr(details, 'matches_played') else None)
                msg3 = str(details.runs_scored if hasattr(details, 'runs_scored') else None)
                msg4 = str(details.wicket_taken if hasattr(details, 'wicket_taken') else None)
            return render_template('index.html', msg='Hello ' + session['fname'] + ', welcome to your dashboard!',
                                   msg2=msg2, msg3=msg3, msg4=msg4, msg5='')


@app_with_orm.route('/predict', methods=['GET', 'POST'])
def predict():
    teams={'Sunrisers Hyderabad':1, 'Mumbai Indians':2, 'Gujarat Lions':3, 'Rising Pune Supergiant':4, 'Royal Challengers Bangalore':5, 'Kolkata Knight Riders':6, 'Delhi Daredevils':7, 'Kings XI Punjab':8, 'Chennai Super Kings':9, 'Rajasthan Royals':10, 'Deccan Chargers':11, 'Kochi Tuskers Kerala':12, 'Pune Warriors':13, 'Rising Pune Supergiants':14, 'Delhi Capitals':15}
    cities = {'Hyderabad':1,'Pune':2,'Rajkot':3,'Indore':4,'Bangalore':5,'Mumbai':6,'Kolkata':7,'Delhi':8,'Chandigarh':9,'Kanpur':10,'Jaipur':11,'Chennai':12,'Cape Town':13,'Port Elizabeth':14,'Durban':15,'Centurion':16,'East London':17,'Johannesburg':18,'Kimberley':19,'Bloemfontein':20,'Ahmedabad':21,'Cuttack':22,'Nagpur':23,'Dharamsala':24,'Kochi':25,'Visakhapatnam':26,'Raipur':27,'Ranchi':28,'Abu Dhabi':29,'Sharjah':30,'Dubai':31,'Mohali':32,'Bengaluru':33 }
    msg5 =''
    uname = session.get("username", "Unknown")
    if uname == "Unknown":
        return redirect(url_for('login'))
    if request.method == 'POST' and 'team1' in request.form and 'team2' in request.form:
            team1 = teams[request.form['team1']]
            team2 = teams[request.form['team2']]
            city =  cities[request.form['city']]
            toss_winn = teams[request.form['toss_winn']]
            input=np.expand_dims(np.array([team1,team2,city,toss_winn]),axis=0)
            print(os.getcwd())
            model = keras.models.load_model(os.path.join(os.getcwd(), "ML/model3.h5"))
            pred = model.predict(input).argmax()
            if pred == 0:
                winner = list(teams.keys())[list(teams.values()).index(team1)]
            else:
                winner = list(teams.keys())[list(teams.values()).index(team2)]
            
            # ML Thing
            #msg5 =
            details = dashboard.query.filter_by(email_id=session['email_id']).first()
            if details == None:
                msg2 = '0'
                msg3 = '0'
                msg4 = '0'
            else:
                msg2 = str(details.matches_played if hasattr(details, 'matches_played') else None)
                msg3 = str(details.runs_scored if hasattr(details, 'runs_scored') else None)
                msg4 = str(details.wicket_taken if hasattr(details, 'wicket_taken') else None)
            return render_template('index.html', msg='Hello ' + session['fname'] + ', welcome to your dashboard!',
                                   msg2=msg2, msg3=msg3, msg4=msg4, msg5=msg5)


@app_with_orm.route('/edit', methods=['GET', 'POST'])
def edit():
    msg = ''
    if request.method == 'GET':
        uname = session.get("username", "Unknown")
        if uname == "Unknown":
            return redirect(url_for('login'))
        else:
            return render_template('details.html')
    elif request.method == 'POST' and 'matches' in request.form and 'runs' in request.form and 'wickets' in request.form:
        email_id = session['email_id']
        matches = request.form['matches']
        runs = request.form['runs']
        wickets = request.form['wickets']

        if not matches or not runs or not wickets:
            msg5 = 'Please enter all the three field to update!'
            return render_template('details.html', msg5=msg5)

        flag = dashboard.query.filter_by(email_id=email_id).first()
        if flag == None:
            user_db = dashboard(email_id=email_id, matches_played=matches, runs_scored=runs, wicket_taken=wickets)
            db.session.add(user_db)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            flag.matches_played = matches
            flag.runs_scored = runs
            flag.wicket_taken = wickets
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('details.html')


if __name__ == "__main__":
    db.create_all()
    app_with_orm.run()
