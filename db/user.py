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
	self.last_activity = self.created

    def set_password(self, password):
        return  generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def login(self, username, password):
        dbsession = sessionmaker(bind=engine)()
        self = dbsession.query(User).filter(User.username == username).first()
        return self.check_password(password)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.username, self.email, self.password)

#create sessionmaker
if __name__ == "__main__":
    dbsession = sessionmaker(bind=engine)()
    user = User(username='team', email='team@six.com',password='six')
    user.metadata.drop_all(engine)
    user.metadata.create_all(engine)
    dbsession.add(user)
    dbsession.commit()
    print user
    print user.check_password('six')
    print user.check_password('6')
    print engine


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

