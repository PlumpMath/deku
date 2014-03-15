#!/usr/bin/env python

#running this script directly will:
#  - drop user database table
#  - recreate user database table with:
#        -- a single user   username: team  pwd: six
from config import engine
from datetime import datetime
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash


#maybe update to pkdb2f later
class User(declarative_base()):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    created = Column(DateTime)

    def __init__(self, username='', password='', email=''):
        self.username = username
        self.email = email
        self.password = self.set_password(password)
	self.created = datetime.utcnow()

    def set_password(self, password):
        return  generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def login(self, username, password):
        dbsession = sessionmaker(bind=engine)()
        tmp = dbsession.query(User).filter(User.username == username).first()
        self.username = tmp.username
        self.email = tmp.email
        self.id = tmp.id
        self.password = tmp.password
        self.created = tmp.created
        return self.check_password(password)

    def __repr__(self):
        return "<User(name='%s', fullname='%s')>" % (self.username, self.email)

    def stringme(self):
        return "name=%s, email=%s"  % (self.username, self.email)

#create sessionmaker
if __name__ == "__main__":
    #create dbsession
    dbsession = sessionmaker(bind=engine)()
    print engine
    #create a sample user to throw into the database
    user = User(username='team', email='team@six.com',password='six')

    #drops the user table if it already exists in the database
    user.metadata.drop_all(engine)

    #(re)creates the user table
    user.metadata.create_all(engine)

    #adds the default user to the database.  user: team   email: team@six.com   password: six
    dbsession.add(user)

    #Actually save all pending changes.
    dbsession.commit()

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

