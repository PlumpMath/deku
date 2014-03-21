#!/usr/bin/env python
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, exc
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from config import DBSession
import re

profile_cols = ['graduation_year','major','classes','biography']
register_cols = ['name', 'email', 'password', 'university']

Base = declarative_base()

#user stuff
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(100,collation='utf8_bin'), nullable=False)
    university = Column(String(100), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    graduation_year = Column(String(10))
    major = Column(String(50))
    classes = Column(String(100))
    biography = Column(String(37777))

    def __init__(self, name='', email='', password='', university =''):
        self.name = name
        self.email = email
        self.password = self.setPassword(password)
        self.university = university

    def setPassword(self, password):
        return  generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return "<User(id='%s',name='%s', email='%s', university='%s', graduation='%s', major='%s', classes='%s', biography='%s')>" % (self.id, self.name, self.email,self.university, self.graduation_year, self.major, self.classes, self.biography)


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
def updateProfile(user, profile):
    if isinstance(profile,dict) and isinstance(user,User):
        for (key,value) in profile.items():
            if key in profile_cols:
                setattr(user, key, value)
    print 'what'

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
    
def DropCreateTable():
    #drops and (re)creates the user table if it already exists in the database
    from config import engine
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


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
    updateProfile(user,dict(biography='wtf',whatever='wta', major='whattttt', graduation_year='2004'))
    
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
