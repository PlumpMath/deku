#!/usr/bin/env python
from sqlalchemy import exc

#from config import *
from config import User, DBSession, DropCreateTable
import re

profile_cols = ['graduation_year','major','classes','biography']
register_cols = ['name', 'email', 'password', 'university']
#pre: name, password, university must be sent in.  email must not be registered yet
#post: registered
def register(dbsession, name, email, password, university):
    validate_results = registerValidate(name, email, password, university)

    if len(validate_results) > 0:
        print 'validationfail'
        return validate_results
    else:
        #try to commit to add commit to database
        user = User(name, email, password, university)
        try:
            dbsession.add(user)
            dbsession.commit()
        except exc.SQLAlchemyError:
            #most likely an error with uniqueness of email.... since we already handled nullable in registerValidate()
            validate_results.append('registration fail: Duplicate email')
            return validate_results
    print user
    return user

#discuss validation criteria
#will return: problems with validations or None
#ie. { username->message, username->message, email->message }
def registerValidate(name, email, password, university):
    errors = []
    if name == '':
        errors.append('no name')
    if len(password) < 6:
        errors.append('Password must be at least 6 characters')
    if not re.match("[^@]+@[^@]+\.[^@]+", email):
        errors.append('Invalid e-mail')
    if university == '':
        errors.append('no university')
    return errors

#user that's from a dbsession must be sent in
def updateProfileByUser(user, fields):
    if isinstance(fields,dict) and isinstance(user,User):
        for (key,value) in fields.items():
            if key in profile_cols:
                setattr(user, key, value)

#user that's from a dbsession must be sent in
def updateProfile(dbsession, user_id, fields):
    print user_id
    user = dbsession.query(User).filter(User.id == user_id).first()
    if user is None:
        return 'user not found in database'
    elif not isinstance(fields,dict):
        return 'fields is not a dict'
    else:
        for (key,value) in fields.items():
            if key in profile_cols:
                setattr(user, key, value)
    return user

#check login and grab fields
#if successful returns True or a message saying why login failed
def login(dbsession, email, password):
    try:
        user = dbsession.query(User).filter(User.email == email).first()        
    except exc.SQLAlchemyError as e:
        print e
        return 'Invalid email'

    if user is None:
        return email + " not registered"
    
    if not user.checkPassword(password):
        return "Invalid password"
    else:
        return user

def addCard(user, category, content, tags):
    pass
    
#DROP and re-CREATE user table and add the single admin
if __name__ == "__main__":
    DropCreateTable()
    
    dbsession = DBSession()

    #register(dbsession, name, email, password, university) 
    #print register('Test', 'test@test.test', 'password', 'UMBC')
    #print register('Test', 'tes2test.test', 'pas', '')
    user =  register(dbsession, 'Test', 'test@test.test', 'password', 'UMBC')
    print user
    #available profile columns are graduation_year, major, classes, graduation_year
    updateProfileByUser(user,dict(biography='wtf',whatever='wta', major='whattttt', graduation_year='2004'))
    
    print user
        
    print 'not yet committed / flushed'
    
    print 'attempting to commit...'
    try:
        result = True
        dbsession.commit()
    except:
        print 'whatever'
        result=False
    finally:
        if not result:
            print 'FAILED TO UPDATE PROFILE'
        else:
            print 'committed'
