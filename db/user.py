#!/usr/bin/env python

#running this script directly will:
#  - drop user database table
#  - recreate user database table with:
#        -- a single user   username: team  pwd: six
from datetime import datetime
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, exc
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from config import DBSession

#user stuff
#notable functions
#login(username, password)   username can be email or username
#register(username, password, email)  not yet validated (will only fail on duplicate username/email)
class User(declarative_base()):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)

    def __init__(self, username='', password='', email=''):
        self.username = username
        self.email = email
        self.password = self.set_password(password)

    def set_password(self, password):
        return  generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    #check login and grab fields
    #if successful returns True or a message saying why login failed
    def login(self, username, password):
        try:
            dbsession = DBSession()
            tmp = dbsession.query(User).filter(User.username == username).first()
        except:
            print ''
        finally:
            dbsession.close()

        if tmp is None:
            return username + " not registered"
        else:
            self.username = tmp.username
            self.email = tmp.email
            self.id = tmp.id
            self.password = tmp.password
            self.created = tmp.created

        if not self.check_password(password):
            return "Invalid password"
        else:
            return True

    #attempt to register user
    #returns: true
    #         OR  invalid_validation_results:
    #                dict(invalid=True, msgs=[])
    #                msgs are a list of the validation failures
    #         OR  sqlalchemyerror(error->msg) )
    def register(self, username, password, email):
        self.__init__(username, password, email)
        validate_results = self.registerValidate()
        if len(validate_results) > 0:
            print 'validationfail'
            return dict(invalid=True, msgs=validate_results)
        else:
            #try to commit to add commit to database
            print 'trycommit'
            try:
                dbsession = DBSession()
                dbsession.add(self)
                dbsession.commit()
            except exc.SQLAlchemyError:
                return dict(sqlerror = exc.SQLAlchemyError)
            finally:
                dbsession.close()
        return True

    #discuss validation criteria
    #will return: problems with validations or None
    #ie. { username->message, username->message, email->message }
    def registerValidate(self):
        errors = []
        try:
            if self.username=='faq':
                errors.append('username is faq')
                print errors
            elif self.username =='badusername':
                errors.append('username is badusername')
            self.password
            self.email
        except NameError:
            errors.append('username, password, or email duznt igzist')
        return errors

    def __repr__(self):
        return "<User(id='%s',name='%s', email='%s')>" % (self.id, self.username, self.email)

    def stringme(self):
        return "id=%s, name=%s, email=%s"  % (self.id, self.username, self.email)


def DropCreateTable():
    #create dbsession
    dbsession = DBSession()
    #create a sample user to throw into the database
    user = User(username='team', email='team@six.com',password='six')

    #drops the user table if it already exists in the database
    from config import engine
    user.metadata.drop_all(engine)

    #(re)creates the user table
    user.metadata.create_all(engine)

    #adds the default user to the database.  user: team   email: team@six.com   password: six
    dbsession.add(user)

    #Actually save all pending changes.
    dbsession.commit()
    dbsession.close()



#DROP and re-CREATE user table and add the single admin
if __name__ == "__main__":
    DropCreateTable()    
#    user = User()
#    print user
#    result = user.register('faw','faw','faw@six.com')
#    try:
#        print result
#        print result.sqlerror
#    except:
#        print ''
#    user.stringme()
#    print user
#    print user.check_password('six')
#    print user.check_password('6')
#    print engine


#print "__________\n"
#user = User()
#print user.login('team','six')
#print user.login('team','seven')
#user2 = User('team','seven')

#user2 = User(username='to', email='two', password='too')
#user3 = User(username='tree', email='three', password = 'three')
#getuser = dbsession.query(User).first()
#print getuser.username
#print getuser.email
#print getuser.password

#print dbsession.add(user)
#print dbsession.add(user2)
#print dbsession.add(user)
#print dbsession.add(user3)
#print user
#print user2
#print dbsession.query(User).filter(User.username.in_(['user','tree'])).all()

#dbsession.add(user)
#dbsession.commit()

#dbsession.add(user)
#try:
#    print dbsession.commit()
#except exc.SQLAlchemyError:
#    print exc.SQLAlchemyError

