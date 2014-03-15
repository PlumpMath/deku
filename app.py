#!/usr/bin/env python
from flask import Flask, render_template, session, request, redirect,jsonify
import db.user

app = Flask(__name__)
app.secret_key="AAAAAAAHHHHHH!!!!!!"

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')



#imitate a failed login post request
@app.route('/fail')
def fail():
    client = app.test_client()
    return client.post('/login', data=dict(username='team', password='password'))
#imitate a succesful login post request
@app.route('/success')
def success():
    client = app.test_client()
    return client.post('/login', data=dict(username='team', password='six'))


#accepts a post request with 'username' and 'password'.  returns.... whatever??? right now just the user name that was logged in + string version of the username and email
#email can also be used as username in the post request (login function in user.py does it)
#will set the session['user'] variable to the user that was logged in.
#I don't think another random server generated user verification is necessary, since flask's session does this already.... not sure if that protects against cookie stealing
#maybe we can add a time based server generated random key to add inside the encrypted cookies if we finish early enough.
@app.route('/login', methods = ['POST'])
def login():
    user = db.user.User()
    if user.login(username = request.form['username'],password =request.form['password']):
        print success
        session['user_name'] = user.username
        session['user_id'] = user.id
        return session['user_name']+": "+user.stringme()
    else:
        print fail
        session.pop("user_name",None)
        session.pop("user_id",None)
    return "FAILED TO LOGON"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
