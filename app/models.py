from app import db
from datetime import datetime
from flask import jsonify

ROLE_USER = 0
ROLE_MOD = 1
ROLE_ADMIN = 2

MAX_CONTENT_LENGTH = 256
class formStruct():
    def __init__(self, *args):
        self.__dict__.update(*args)
    
    
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(64), index = True, unique = False)
    lastName = db.Column(db.String(128), index = True, unique = False)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    email = db.Column(db.String(128), index = True, unique = True)
    password = db.Column(db.LargeBinary(60))
    univ = db.Column(db.String(100))
    cards = db.relationship('Card', backref = 'user', cascade='all,delete', lazy = 'dynamic')
    profile = db.relationship('Profile', uselist=False, backref="user")
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % (str(self.id)+" "+self.firstName + " " + self.lastName)

    @property
    def serialize(self):
        # Return User data in a serializable format
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "role": self.role
        }

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    year = db.Column(db.String(10))
    major = db.Column(db.String(50))
    classes = db.Column(db.String(100))
    bio = db.Column(db.String(33777))
    def __repr__(self):
        return '<Profile %r>' %(str(self.user.id) + " " + self.major)

class Card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(MAX_CONTENT_LENGTH))
    #timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Card %r>' % (self.content[:40] + "...")

    @property
    def serialize(self):
        # Return Card data in a serializable format
        return {
            "content": self.content,
            "created_at": self.timestamp,
            "author_id": self.user_id
        }

