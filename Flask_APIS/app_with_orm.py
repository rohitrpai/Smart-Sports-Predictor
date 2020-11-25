import re
from datetime import datetime

import MySQLdb.cursors
from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime

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
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            msg = 'Please enter your username/password!'
            return render_template('login.html', msg=msg)
        account = users.query.filter_by(user_name=username, password=password).first()
        if account:
            session['loggedin'] = True
            # session['id'] = account['id']
            # session['username'] = account['username']
            # session['fname'] = account['first_name']
            msg = 'Logged in successfully !'
            return redirect(url_for("home"))
        else:
            msg = 'Incorrect username / password !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    elif request.method == 'GET':
        uname = session.get("username", "Unknown")
        if uname == "Unknown":
            return render_template('login.html')
        else:
            return redirect(url_for("home"))
    return render_template('login.html', msg=msg)


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
        return render_template('index.html')
        '''uname = session.get("username", "Unknown")
        if uname == "Unknown":
            return render_template('login.html', msg='You need to sign in!')
        else:
            return render_template('index.html', msg='Hello ' + session['fname'] + ', welcome to your dashboard!')'''
    '''elif request.method == 'POST' or request.method == 'GET':
        msg = 'Failed'
        return msg'''
    # Implement dropdown ML thing


if __name__ == "__main__":
    db.create_all()
    app_with_orm.run()
