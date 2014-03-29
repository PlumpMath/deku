#!/usr/bin/env python
import os

from flask import Flask, render_template, url_for, session, request, redirect,jsonify, g, json
from db.config import DBSession
import db.user
import db.config
import db.card
import re

app = Flask(__name__)
app.secret_key=os.urandom(777)

#session_scope is wrapper for things that need a dbsession
from contextlib import contextmanager
@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    dbsession = DBSession()
    try:
        yield dbsession
        dbsession.commit()
    except:
        dbsession.rollback()
        raise
    finally:
        dbsession.close()
        
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
        return redirect(url_for('index'), code=304)
    else:
        dbsession = DBSession()
        result = db.user.login(dbsession, email = request.form['email'],password =request.form['password'])
        if isinstance(result,db.user.User):
            session['first_name'] = result.firstname
            session['last_name'] = result.lastname
            session['user_id'] = result.id
            session['logged_in'] = True
            return jsonify(dict(login='true'))
        else:
            session.clear()
            session['result'] = result
            return ''
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

#accepts post request with
#required:
#    name, email, password, university
#optional:
#    graduation_year, major, classes, biography
@app.route('/register',methods = ['POST'])
def register():
    print 'REGISTER'
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    university = request.form['university']
    
    #validate
    errors = []
    if firstname == '':
        errors.append('no first name')
    if lastname == '':
        errors.append('no last name')
    if len(password) < 6:
        errors.append('Password must be at least 6 characters')
    if not re.match("[^@]+@[^@]+\.[^@]+", email):
        errors.append('Invalid e-mail')
    if university == '':
        errors.append('no university')
    #if there are errors, return them
    if len(errors) > 0:
        return jsonify(errors=errors)

    #grab user if registered
    with session_scope() as dbsession:
        user = dbsession.query(db.config.User).filter(db.config.User.email == email).first()
        
    #if already registered, don't register
    if isinstance(user, db.user.User):
        return jsonify(errors="Already registered")
    
    user = db.config.User(firstname, lastname, email, password, university)

    #register user and
    #return session_id to use for edit profileprint user
    with session_scope() as dbsession:
        dbsession.add(user)
        dbsession.commit()
        session['user_id'] = user.id
        
    return jsonify(dict(data=""))

#allows a user to edit his own profile
@app.route('/editprofile', methods = ['POST'])
def editprofile():
    print 'asdf'
    if 'user_id' not in session:
        print 'fail user session'
        return dict(error="not logged in/registering")

    fields = dict()
    if 'year' in request.form:
        fields['year']=request.form['year']
    if 'major' in request.form:
        fields['major']=request.form['major']
    if 'classes' in request.form:
        fields['classes']=request.form['classes']
    if 'bio' in request.form:
        fields['bio']=request.form['bio']
        
    #get and update fields
    with session_scope() as dbsession:
        user = dbsession.query(db.config.User).filter(db.config.User.id == session['user_id']).first()      
        user.update(fields)
        
    return jsonify(dict(data="")) 

@app.route('/addcard', methods=['POST'])
def addcard():
    print 'ADDCARD'
    
    #make sure user is logged in
    if 'logged_in' not in session:
        return "User must be logged in" 

    category = request.form['category']
    content = request.form['content']
    tags = request.form['tags']

    tags = json.loads(tags)

    with session_scope() as dbsession:
        user = dbsession.query(db.config.User).filter(db.config.User.id == session['user_id']).first()
        card = db.config.Card()
        print card
        card.content = content
        print card
        card.category = category
        print card
        user.cards.append(card)
        print card
        for tag in tags:
            print tag
            tag = db.config.Tag(tag)
            card.tags.append(tag)
            print card
        print card
    return jsonify(dict(data=""))

@app.route('/getCards')
def getCards():
    number = request.args.get('numCards')
    dbsession = DBSession()
    deck =  db.card.getLastCards(dbsession, number)
    print "Faq"
    print deck
    print "Faq"
    print "----------------"
    for card in deck:
        print card
        print "\n\n"
    print "------------------"
    return ''

@app.route('/test/login/status')
def testLoginStatus():
    if 'user_name' in session and 'user_id' in session:
        return 'LOGGED IN AS: ' + session['user_name']
        #return 'Username: '+session['user_name'] + ' id: '+str(session['user_id'])
    else:
        return 'False'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

