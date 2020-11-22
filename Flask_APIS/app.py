from flask import Flask, render_template, request, redirect, url_for, session 
from flask_mysqldb import MySQL
import MySQLdb.cursors 
import re
import yaml

from flask_injector import FlaskInjector
from injector import inject
from Flask_APIS.Service import MyService
from Flask_APIS.dependencies import configure
  
  
app = Flask(__name__)

#db = yaml.load(open('db.yaml'))
  
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
@app.route('/main', methods =['GET', 'POST'])
def main():
    if request.method == 'GET':
        uname = session.get("username", "Unknown")
        if uname == "Unknown":
            return render_template('main.html')
        else:
            return redirect(url_for("home"))


@inject
@app.route('/login', methods =['GET', 'POST'])
def login(service: MyService):
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            msg = 'Please enter your username/password!'
            return render_template('login.html', msg=msg)
        #cursor = service.get_db_cursor()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", [username, password])
        account = cursor.fetchone()
        if account: 
            session['loggedin'] = True
            #session['id'] = account['id']
            session['username'] = account['username']
            session['fname'] = account ['first_name']
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
    return render_template('login.html', msg = msg)


@app.route('/logout') 
def logout(): 
    session.pop('loggedin', None) 
    session.pop('id', None) 
    session.pop('username', None) 
    return redirect(url_for('login')) 


@inject
@app.route('/register', methods =['GET', 'POST']) 
def register(service: MyService):
    msg = '' 
    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        #cursor = service.get_db_cursor()
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
            cursor.execute("INSERT INTO users(first_name,last_name,username,password,email_id) VALUES (% s, % s,% s, % s, % s)", [firstname, lastname, username, password, email])
            #service.get_sql_instance().connection.commit()
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
    return render_template('registration.html', msg = msg)


@app.route('/home', methods =['GET', 'POST'])
def home():
    msg = ''
    if request.method == 'GET':
        uname = session.get("username", "Unknown")
        if uname == "Unknown":
            return render_template('login.html', msg='You need to sign in!')
        else:
            return render_template('index.html', msg='Hello, '+session['fname']+'!')
    '''elif request.method == 'POST' or request.method == 'GET':
        msg = 'Failed'
        return msg'''
    #Implement dropdown ML thing


FlaskInjector(app=app, modules=[configure])


if __name__ == "__main__":
    app.run()