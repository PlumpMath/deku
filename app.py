#!/usr/bin/env python
from flask import Flask, render_template, session, request, redirect,jsonify, g
from db.config import DBSession
import db.user

app = Flask(__name__)
app.secret_key="AAAAAAAHHHHHH!!!!!!"

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

#accepts a post request with 'username' and 'password'.
#precondition: none
#postcondition: session['user_name'] and session['user_id'] will be set to their correct values, or the session will be cleared
@app.route('/login', methods = ['POST'])
def login():
    user = db.user.User()
    result = user.login(username = request.form['username'],password =request.form['password'])
    if result != True:
        session.clear()
        return result
    else:
        session['user_name'] = user.username
        session['user_id'] = user.id
        return session['user_name']+": "+user.stringme()

@app.route('/register', methods = ['POST'])
def register():
    user = db.user.User()
    un = request.form['username']
    pw = request.form['password']
    em = request.form['email']
    print un
    print pw
    print em
    result = user.register(username = request.form['username'], password=request.form['password'], email=request.form['email'])
    
    if result is True:
        print '--------stored-------'
        return 'stored'
    else:
        print '-------error---------'
        print result
        return ''


#test login
@app.route('/test/login')
def testLogin():
    client = app.test_client()
    print client.post('/login', data=dict(username='team', password='six')).data
    print "OK" +client.get('/test/login/status').data
    print client.post('/login', data=dict(username='teaM', password='six')).data
    print "OK" +client.get('/test/login/status').data
    print client.post('/login', data=dict(username='team', password='SiX')).data
    print "NONE" +client.get('/test/login/status').data
    print client.post('/login', data=dict(username='TEAM', password='six')).data
    print "OK"+client.get('/test/login/status').data
    print client.post('/login', data=dict(username='teaaaaaam', password='six')).data
    print "NONE"+client.get('/test/login/status').data
    return ""

@app.route('/test/login/status')
def testLoginStatus():
    if 'user_name' in session and 'user_id' in session:
        return 'Username: '+session['user_name'] + '  id: '+str(session['user_id'])
    else:
        return 'None'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
