from app import db
from datetime import datetime
import base64
import time

ROLE_USER = 0
ROLE_MOD = 1
ROLE_ADMIN = 2
MAX_CONTENT_LENGTH = 256


marked = db.Table('marked',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('card_id', db.Integer, db.ForeignKey('card.id'))
)

added = db.Table('added',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('card_id', db.Integer, db.ForeignKey('card.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(64), index = True, unique = False)
    lastName = db.Column(db.String(128), index = True, unique = False)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    email = db.Column(db.String(128), index = True, unique = True)
    password = db.Column(db.LargeBinary(60))
    university = db.Column(db.String(128))
    profile = db.relationship('Profile', uselist=False, backref='user')
    cards = db.relationship('Card', backref = 'author', cascade='all,delete', lazy = 'dynamic')
    courses = db.Column(db.String(MAX_CONTENT_LENGTH))
    comments = db.relationship('Comment', backref='author')
    markedCards = db.relationship('Card', secondary="marked", backref="marker")
    addedCards = db.relationship('Card', secondary="added", backref="adder")

    def __repr__(self):
        return '<User %r>' % (self.firstName + " " + self.lastName)

    @property
    def serialize(self):
        # Return User data in a serializable format
        return {
            "id": self.id,
            "role": self.role,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "university": self.university,
            "bio": self.profile.bio,
            "classes": self.courses.split(","),
            "grad_year": self.profile.grad_year,
            "major": self.profile.major,
            "avatar": base64.b64encode(self.profile.avatar)
        }

    @property
    def get_avatar(self):
        return base64.b64encode(self.profile.avatar)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    grad_year = db.Column(db.String(5))
    major = db.Column(db.String(17))
    bio = db.Column(db.String(MAX_CONTENT_LENGTH))
    avatar = db.Column(db.LargeBinary())
    
    def __repr__(self):
        return '<Profile %r>' % (str(self.user.id) + " " + str(self.major))

    @property
    def serialize(self):
        return {
            "id": self.id,
            "user id": self.user_id,
            "grad_year": self.grad_year,
            "major": self.major,
            "biography": self.bio,
        }

class Card(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(MAX_CONTENT_LENGTH))
    category = db.Column(db.String(MAX_CONTENT_LENGTH))
    tags = db.Column(db.String(MAX_CONTENT_LENGTH))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    userFirst = db.Column(db.String(MAX_CONTENT_LENGTH))
    userLast = db.Column(db.String(MAX_CONTENT_LENGTH))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='card', cascade='all,delete', lazy='dynamic')
    popularity = db.Column(db.Integer)

    def __repr__(self):
        return '<Card %r>' % (self.content[:40] + "...")

    @property
    def serialize(self):
        # Return Card data in a serializable format
        return {
            "id": self.id,
            "content": self.content,
            "category": self.category,
            "created_at": self.timestamp,
            "authorFirst": self.userFirst,
            "authorLast": self.userLast,
            "author_id": self.user_id,
            "tags": self.tags.split(",")
        }


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_id = db.Column(db.Integer)
    to_id = db.Column(db.Integer)
    message = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    
    @property
    def serialize(self):
        fr = User.query.filter(User.id==self.from_id).first()
        to = User.query.filter(User.id==self.to_id).first()
        return {
            "to_id": self.to_id,
            "to": to.firstName + " " + to.lastName,
            "from_id": self.from_id,
            "from": fr.firstName + " " + fr.lastName,
            "message": self.message,
            "timestamp": self.timestamp
        }

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    content = db.Column(db.String(MAX_CONTENT_LENGTH))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())

    @property
    def serialize(self):
        author = models.User.query.get(int(self.author_id))
        return {
            "author_id": self.author_id,
            "author_first": author.firstName,
            "author_last": author.lastName, 
            "content": self.content,
            "timestamp": self.timestamp
        }
