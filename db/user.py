#!/usr/bin/env python
from sqlalchemy import exc

#from config import *
from config import User, DBSession, DropCreateTable, Tag, Card
import re

profile_cols = ['graduation_year','major','classes','biography']
register_cols = ['name', 'email', 'password', 'university']
#pre: name, password, university must be sent in.  email must not be registered yet
#post: registered
def register(dbsession, name, email, password, university):
    validate_results = registerValidate(name, email, password, university)
    
    #check if exists
    user = dbsession.query(User).filter(User.email == email).first()
    
    if user is None:
        if len(validate_results) > 0:
            print 'validationfail'
            return validate_results
        else:
            user = User(name, email, password, university)
        return user
    else:
        validate_results.append('registration fail: Duplicate email')
        return validate_results 

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
    user = getUser(dbsession, user_id)
    
    if not isinstance(fields,dict):
        raise Exception('fields is not a dict')
    else:
        for (key,value) in fields.items():
            if key in profile_cols:
                setattr(user, key, value)
    return user

#check login and grab fields
#if successful returns True or a message saying why login failed
def login(dbsession, email, password):
    user = dbsession.query(User).filter(User.email == email).first()        

    if user is None:
        return 'user not registered'
    
    if not user.checkPassword(password):
        return "Invalid password"
    else:
        return user

def addCard(dbsession, user_id, category, content, tags):
    #user = getUser(dbsession, user_id)
    card = Card(user_id=user_id, category=category, content = content)
    for it in tags:
        card.tags.append(Tag(tag=it))
    print card.tags
    user = getUser(dbsession, user_id)
    user.cards.append(card)
    print user.cards
    #card = Card(user_id=user_id, category=category, content=content)
    #for it in tags:
        #card.tags.append(Tag(tag=it))
        #print card.tags
    #user.cards.append(Card(category=category, content=content))
    #return user
    
def getUser(dbsession, user_id):
    user = dbsession.query(User).filter(User.id == user_id).first()
    if user is None:
        raise Exception('user not found in database')
    return user
    
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
