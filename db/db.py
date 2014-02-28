#!/usr/bin/env python

import datetime
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
#from sqlalchemy import exc

# mysql db info
dbhost='localhost'
dbuser='root'
dbpass='pass'
dbname='db'
DB_URI = 'mysql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' + dbname


#Base = declarative_base()


#from sqlalchemy.ext.declarative import declarative_base
#from werkzeug.security import generate_password_hash, check_password_hash
#table schema
class User(declarative_base()):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    admin = Column(Integer, default=0)

    def __init__(self, username, password, email, admin):
        self.admin = admin
        self.username = username
        self.email = email
        self.password = self.set_password(password)

    def set_password(self, password):
        return  generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.username, self.email, self.password)

#class profile(Base):
#    __tablename__ = 'user2'
#
#    id = Column(Integer, primary_key=True)
#    user_id = Column(Integer, ForeignKey('users.id'))
#    profile = Column(String(50))

def wtfff():
    return 'wtf'


#create engine
engine = create_engine(DB_URI)

#create tables
#Base.metadata.create_all(engine)
#User().metadata.create_all(engine)
#create user
#user = User(username='username', email='email', password='password')

#create sessionmaker
Session = sessionmaker(bind=engine)


dbsession = Session()
user = User(username='team', email='team@six.com',password='six', admin=1)
user.metadata.create_all(engine)
dbsession.add(user)
dbsession.commit()
print user
print user.check_password('six')
print user.check_password('6')
print engine

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

