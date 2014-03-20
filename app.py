#!/usr/bin/env python
import os

from flask import Flask, render_template, url_for, session, request, redirect,jsonify, g
from db.config import DBSession
import db.user

app = Flask(__name__)
app.secret_key=os.urandom(777)

@app.route('/')
@app.route('/index')
def index():
    print 'INDEX'
    g.result = session.pop('result', None)
    return render_template('index.html')

#accepts a post request with 'username' and 'password'.
#precondition: none
#postcondition: session['user_name'] and session['u    ser_id'] will be set to their correct values, or the session will be cleared
@app.route('/login', methods = ['POST'])
def login():
    #user = db.user.User()
    print 'login'
    if (request.form['email'] == 'admin@deku.com' and request.form['password'] == 'password'):
        print 'LOGIN THE ADMIN USER'
        session['user_name'] = "Administrator"
        session['logged_in'] = True
        return redirect(url_for('/index', code=304))
    else:
        dbsession = DBSession()
        email = '|'+request.form['email']+'|'
        password = '|'+request.form['password']+'|'
        result = db.user.login(dbsession, email = request.form['email'],password =request.form['password'])
        print result
        if isinstance(result,db.user.User):
            session['user_name'] = result.name
            session['user_id'] = result.id
            session['logged_in'] = True
            return redirect('/index', code=304)
        else:
            session.clear()
            session['result'] = result
            return redirect('/index', code=304)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/register', methods = ['POST'])
def register():
    #register function works
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    university = request.form['university']
    print db.user.register(name, email, password, university)
    return 'done registering'

@app.route('/editprofile', methods = ['POST'])
def editprofile():
    dbsession = DBSession()
    fields = dict()
    for key in db.user.profile_cols:
        if key in request.form:
            value = request.form[key]
            fields[key] = value
            
    user = dbsession.query(db.user.User).filter_by(id = session['user_id']).first()
    db.user.updateProfile(user, fields)
    
    if user is None:
        raise Exception("user must be logged in")
        return 'user must be logged in'
    else:
        try:
            dbsession.commit()
            print 'commit'
        except:
            return 'some kind of sql error' 
        finally:
            dbsession.close()
        return 'profile updated'
    

@app.route('/test/login/status')
def testLoginStatus():
    if 'user_name' in session and 'user_id' in session:
        return session['user_name']
        #return 'Username: '+session['user_name'] + ' id: '+str(session['user_id'])
    else:
        return 'False'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

