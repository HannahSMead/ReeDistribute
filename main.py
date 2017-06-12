from flask import Flask, render_template, request

import schema
from controls import create_student, create_donor, authenticate
import db
app = Flask(__name__)
app.debug = True 

@app.route('/')
def home():
    schema.start_db()
    return render_template('frontpage.html')

@app.route('/create_account')
def create_account():
    return render_template('addform.html')

@app.route('/record_account', methods=['POST'])
def add_account():
    username=request.form['username']
    name =request.form['name']
    email=request.form['email']
    pw1 =request.form['pw1']
    pw2 =request.form['pw2']
    

    if (pw1 == pw2):
        create_student(username, name, pw1, email)

        return render_template('frontpage.html') 
    else: 
        return render_template('addform.html')

@app.route('/login')
def log_in():
    return render_template('login.html')


@app.route('/are-you-real', methods=['POST'])
def check_credentials():
    usernameAttempt = request.form['uname']
    passwordAttempt = request.form['psw']
    result = authenticate(usernameAttempt, passwordAttempt)
    if result: return render_template('loginsuccess.html')
    else: return render_template("loginFailure.html")


if __name__ == '__main__':
    app.run()