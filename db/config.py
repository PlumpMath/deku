#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

# mysql db info
dbuser='root'
dbpass='pass'
dbname='db'
dbhost='localhost'
DB_URI = 'mysql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' + dbname + '?charset=utf8'

engine = create_engine(DB_URI, encoding='utf8')
DBSession = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(100,collation='utf8_bin'), nullable=False)
    university = Column(String(100), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    graduation_year = Column(String(10))
    major = Column(String(50))
    classes = Column(String(100))
    biography = Column(String(37777))
    
    cards = relationship('Card', cascade="all,delete", backref="user")

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
    def stringme(self):
        return "<User(id='%s',name='%s', email='%s', university='%s', graduation='%s', major='%s', classes='%s', biography='%s')>" % (self.id, self.name, self.email,self.university, self.graduation_year, self.major, self.classes, self.biography)
    
class Card(Base):
    __tablename__ = 'card'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    category = Column(String(77), nullable=True, index=True)
    content = Column(String(34567), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    tags = relationship('Tag', cascade="all,delete", backref="card")
    def __repr__(self):
        return "[CARD][id=%s][category=%s][content=%s][tags=%s]"%(self.id, self.category, self.content, self.tags)

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey('card.id'), nullable=False)
    tag = Column(String(37), nullable=False, index=True)

    def __repr__(self):
        return "[TAG][id=%s][parent=%s][tag=%s]"%(self.id, self.parent_id, self.tag)

def DropCreateTable():
    #drops and (re)creates the user table if it already exists in the database
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    