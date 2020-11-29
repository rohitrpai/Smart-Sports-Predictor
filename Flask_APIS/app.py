import re

import MySQLdb.cursors
from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_injector import FlaskInjector
from flask_mysqldb import MySQL
from injector import inject

from Flask_APIS.Service import MyService
from Flask_APIS.dependencies import configure

app = Flask(__name__)
Bootstrap(app)

# db = yaml.load(open('db.yaml'))

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Smart@1010'
app.config['MYSQL_DB'] = 'predictor'

mysql = MySQL(app)


@inject
@app.route('/data')
def get_data(service: MyService):
    print(f"MyService instance is {service}")
    return service.get_data()


@app.route('/')
@app.route('/main', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        uname = session.get("username", "Unknown")
        if uname == "Unknown":
            return render_template('main.html')
        else:
            return redirect(url_for("home"))


@inject
@app.route('/login', methods=['GET', 'POST'])
def login(service: MyService):
    msg = ''
    status = 200
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            msg = 'Please enter your username/password!'
            status = 401
            return render_template('login.html', msg=msg), status
        # cursor = service.get_db_cursor()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", [username, password])
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            # session['id'] = account['id']
            session['username'] = account['username']
            session['fname'] = account['first_name']
            session['email_id'] = account['email_id']
            msg = 'Logged in successfully !'
            return redirect(url_for("home"))
        else:
            msg = 'Incorrect username / password !'
            status=404
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
        status=404
    elif request.method == 'GET':
        uname = session.get("username", "Unknown")
        if uname == "Unknown":
            return render_template('login.html')
        else:
            return redirect(url_for("home"))
    return render_template('login.html', msg=msg), status


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@inject
@app.route('/register', methods=['GET', 'POST'])
def register(service: MyService):
    msg = ''
    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # cursor = service.get_db_cursor()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s", [username])
        account = cursor.fetchone()
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
            cursor.execute(
                "INSERT INTO users(first_name,last_name,username,password,email_id) VALUES (% s, % s,% s, % s, % s)",
                [firstname, lastname, username, password, email])
            # service.get_sql_instance().connection.commit()
            mysql.connection.commit()
            cursor.close()
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


@app.route('/home', methods=['GET', 'POST'])
def home():
    msg = ''
    if request.method == 'GET':
        uname = session.get("username", "Unknown")
        if uname == "Unknown":
            return redirect(url_for('login'))
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM dashboard WHERE email_id = %s", [session['email_id']])
            details = cursor.fetchone()
            if details == None:
                msg2 = '0'
                msg3 = '0'
                msg4 = '0'
            else:
                msg2 = str(details['matches_played'])
                msg3 = str(details['runs_scored'])
                msg4 = str(details['wicket_taken'])
            return render_template('index.html', msg='Hello ' + session['fname'] + ', welcome to your dashboard!', msg2=msg2, msg3=msg3, msg4=msg4)
    '''elif request.method == 'POST' or request.method == 'GET':
        msg = 'Failed'
        return msg'''
    # Implement dropdown ML thing


@app.route('/edit', methods=['GET', 'POST'])
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

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM dashboard WHERE email_id = %s", [email_id])
        flag = cursor.fetchone()
        if flag == None:
            cursor.execute("INSERT INTO dashboard(email_id, matches_played, runs_scored, wicket_taken) VALUES(%s, %s, %s, %s)",[email_id, matches, runs, wickets])
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('home'))
        else:
            cursor.execute("UPDATE dashboard SET matches_played=%s, runs_scored=%s, wicket_taken=%s WHERE email_id=%s",[matches, runs, wickets, email_id])
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('home'))
    return render_template('details.html')


FlaskInjector(app=app, modules=[configure])

if __name__ == "__main__":
    app.run()
