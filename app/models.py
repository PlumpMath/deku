from app import db
from datetime import datetime
from flask import jsonify

ROLE_USER = 0
ROLE_MOD = 1
ROLE_ADMIN = 2
MAX_CONTENT_LENGTH = 256

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(64), index = True, unique = False)
    lastName = db.Column(db.String(128), index = True, unique = False)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    email = db.Column(db.String(128), index = True, unique = True)
    password = db.Column(db.LargeBinary(60))
    university = db.Column(db.String(128))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    profile = db.relationship('Profile', uselist=False, backref='user')
    cards = db.relationship('Card', backref = 'author', cascade='all,delete', lazy = 'dynamic')
    courses = db.relationship('Course', backref='user', cascade = 'all,delete')

    def __repr__(self):
        return '<User %r>' % (self.firstName + " " + self.lastName)

    @property
    def serialize(self):
        # Return User data in a serializable format
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "university": self.university,
            "bio": self.profile.bio,
            "classes": [course.id for course in self.profile.courses],
            "grad_year": self.profile.grad_year,
            "major": self.profile.major,
            "role": self.role,
            "cards": [card.id for card in self.cards]
            
        }
        
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    grad_year = db.Column(db.String(5))
    major = db.Column(db.String(17))
    bio = db.Column(db.String(77))
    courses = db.relationship('Course', backref='profile')
    
    def __repr__(self):
        return '<Profile %r>' %(str(self.user.id) + " " + str(self.major))

    @property
    def serialize(self):
        return {
            "id": self.id,
            "user id": self.user_id,
            "grad_year": self.grad_year,
            "major": self.major,
            "classes": [course.id for course in self.courses],
            "biography": self.bio
        }
        
class Course(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    course = db.Column(db.String(50))
    
    @property
    def serialize(self):
        return{
            "class": self.course
        }

class Card(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(MAX_CONTENT_LENGTH))
    category = db.Column(db.String(MAX_CONTENT_LENGTH))
    tags = db.relationship('Tag', cascade="all,delete", backref="card")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref = 'card', cascade='all,delete', lazy = 'dynamic')
    def __repr__(self):
        return '<Card %r>' % (self.content[:40] + "...")

    @property
    def serialize(self):
        # Return Card data in a serializable format
        card= {
            "id": self.id,
            "content": self.content,
            "category": self.category,
            "created_at": self.timestamp,
            "author_id": self.user_id,
            "tags": [tag.id for tag in self.tags],
            "comments": [comment.id for comment in self.comments]
        }
        return card

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    tag = db.Column(db.String(37), nullable=False, index=True)

    @property
    def serialize(self):
        return {
            "tag": self.tag,
            "id": self.id,
            "card_id": self.card
        }
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    comment = db.Column(db.String, nullable=False)
    
    @property
    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "card_id": self.card_id,
            "comment": self.comment
        }
    
    
