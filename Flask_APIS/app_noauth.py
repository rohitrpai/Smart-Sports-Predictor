import re

import MySQLdb.cursors
from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap

app_noauth = Flask(__name__)
Bootstrap(app_noauth)


@app_noauth.route('/')
@app_noauth.route('/main', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        uname = session.get("username", "Unknown")
        if uname == "Unknown":
            return render_template('main.html')
        else:
            return redirect(url_for("home"))


@app_noauth.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            msg = 'Please enter your username/password!'
            return render_template('login.html', msg=msg)
        else:
            return redirect((url_for('home')))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    elif request.method == 'GET':
        uname = session.get("username", "Unknown")
        if uname == "Unknown":
            return render_template('login.html')
        else:
            return redirect(url_for("home"))
    return render_template('login.html', msg=msg)


@app_noauth.route('/logout')
def logout():
    return redirect(url_for('login'))


@app_noauth.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if not firstname or not lastname or not username or not password or not email:
            msg = 'Please fill out the form !'
        elif not re.match(r'[A-Za-z]', firstname):
            msg = 'First Name must contain only alphabets!'
        elif not re.match(r'[A-Za-z]', lastname):
            msg = 'Last Name must contain only alphabets!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    elif request.method == 'GET':
        uname = session.get("username", "Unknown")
        if uname == "Unknown":
            return render_template('registration.html')
        else:
            return redirect(url_for("home"))
    return render_template('registration.html', msg=msg)


@app_noauth.route('/home', methods=['GET', 'POST'])
def home():
    msg = ''
    if request.method == 'GET':
        return render_template('index.html', msg='Hello!')
    # Implement dropdown ML thing


if __name__ == "__main__":
    app_noauth.run()
