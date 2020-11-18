from flask import Flask, render_template, request, redirect, url_for, session 
from flask_mysqldb import MySQL
import MySQLdb.cursors 
import re 
  
  
app = Flask(__name__) 
  
  
app.secret_key = 'your secret key'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'dbregistration'
  
mysql = MySQL(app) 

@app.route('/')
@app.route('/main', methods =['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('main.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = '' 
    if request.method == 'POST' and 'Uname' in request.form and 'Pass' in request.form:
        username = request.form['Uname']
        password = request.form['Pass']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, )) 
        account = cursor.fetchone()
        if account: 
            session['loggedin'] = True
            session['id'] = account['id'] 
            session['username'] = account['username'] 
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg) 
        else:
            msg = 'Incorrect username / password !'
    elif request.method == 'POST' and 'Uname' not in request.form or 'Pass' not in request.form:
        msg = 'Please enter your username/password!'
    return render_template('login.html', msg = msg)


@app.route('/logout') 
def logout(): 
    session.pop('loggedin', None) 
    session.pop('id', None) 
    session.pop('username', None) 
    return redirect(url_for('login')) 


@app.route('/register', methods =['GET', 'POST']) 
def register():
    msg = '' 
    if request.method == 'POST' and 'Uname' in request.form and 'Pass' in request.form and 'Email_id' in request.form :
        username = request.form['Uname']
        password = request.form['Pass']
        email = request.form['Email_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, )) 
        account = cursor.fetchone() 
        if account: 
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username): 
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email: 
            msg = 'Please fill out the form !'
        else: 
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, )) 
            mysql.connection.commit() 
            msg = 'You have successfully registered !'
    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
    return render_template('registration.html', msg = msg)


@app.route('/home', methods =['GET', 'POST'])
def home():
    msg = ''
    if request.method == 'POST' or request.method == 'GET':
        return render_template('index.html', msg = msg)


if __name__ == "__main__":
    app.run()