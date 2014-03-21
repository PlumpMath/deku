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
        return redirect(url_for('index'), code=304)
    else:
        dbsession = DBSession()
        result = db.user.login(dbsession, email = request.form['email'],password =request.form['password'])
        print result
        if isinstance(result,db.user.User):
            session['user_name'] = result.name
            session['user_id'] = result.id
            session['logged_in'] = True
            return redirect(url_for('index'), code=304)
        else:
            session.clear()
            session['result'] = result
            return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


#accepts post request with
#required:
#    name, email, password, university
#optional:
#    graduation_year, major, classes, biography
@app.route('/register')#, methods = ['POST'])
def register():
    ####################DUMMYTESTDATA
    name='f'
    email='asdf@fjaiwfaewji.aw'
    password='ffffff'
    university='f'
    fields=dict(classes="are",major="pain",innn="the",biography="face",graduation_year="1973")
    #DUMMYTESTDATA###################
    ####################REALDATAA?#
    #name = request.form['name']
    #email = request.form['email']
    #password = request.form['password']
    #university = request.form['university']
    #get all fields to send into profile, profile will ignore unneeded fields
    #fields = request.form
    #REALDATAA?####################
    print fields

    dbsession = DBSession()
    #register user    
    result = db.user.register(dbsession, name, email, password, university)
    
    #update profile if registering successful
    if isinstance(result, db.user.User):  #result is a User so let's update that profile
        #pass in user and profile fields to update
        db.user.updateProfileByUser(result, fields)
        print 'registered' + result.name + 'now let\'s update profile...'
        try:
            #commit update
            dbsession.commit()
        except:
            print 'ion'
        print 'profile updated'
        return 'something'
    else:#register() returned an error
        return name + ' NOT CREATED: ' + str(result)

@app.route('/editprofile')#, methods = ['POST'])
def editprofile():
    #if 'user_id' not in session:
        #raise Exception("user must be logged in")
    #fields=request.form()
    #user_id = session['user_id']
    user_id='2'
    fields=dict(classes="allour",major="bases",innn="bases",biography="arebelong",graduation_year="2us")
    
    dbsession = DBSession()

    #call function, pass in dbsession, user_id and fields in profile to update
    result = db.user.updateProfile(dbsession, user_id, fields)
    print result
    if not result:
        raise Exception(result)
    try:
        dbsession.commit()
    except:
        raise Exception('some sql error')
    return result.name + ': classes[' + result.classes + '] major[' + result.major + '] biography[' + result.biography + '] graduation[' + result.graduation_year+']' 

@app.route('/addcard')#, methods=['POST'])
def addcard():
    ####################DUMMYTESTDATA
    category='f'
    content='asdf@fjaiwfaewji.aw'
    tags=list('ffffff','gggg','hhhh')
    #DUMMYTESTDATA###################
    ####################REALDATAA?#
    #category = request.form['category']
    #content = request.form['content']
    #tags = request.form['tags']
    #REALDATAA?####################
    print 'adding post...'
    
    dbsession = DBSession()
    #get user by session['user_id']
    #result = db.user.addCard(dbsession, user_id, category, )
    user = dbsession.query(db.user.User).filter_by(id == session['user_id']).first()
    
    if user is None:
        print 'Nothing done, user must be logged in'
        return 'Nothing done, user must be logged in'
    else:
        #addCard(user, category, content, tags)
        try:
            dbsession.commit()
            print 'commit'
        except:
            return 'some kind of sql error' 
        finally:
            dbsession.close()
        return 'profile updated'
    
        
    return 'some stuff'


@app.route('/test/login/status')
def testLoginStatus():
    if 'user_name' in session and 'user_id' in session:
        return session['user_name']
        #return 'Username: '+session['user_name'] + ' id: '+str(session['user_id'])
    else:
        return 'False'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

