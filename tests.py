#!.venv/bin/python
import os
import unittest
import urllib2

from flask import json
from config import basedir
from app import app, db, bcrypt, session
from app.models import User, Card

class APITestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

# Test /deku/api/users POST

    def test_post_new_user(self):
        print '----------NEW USER1-----------'
        response = self.app.post('/deku/api/users', data = dict(firstName="Jane", lastName="Doe", email="janedoe@email.com", password="password1", university="UMBC"))
        self.assertEquals(response.status_code, 201)
        print response.data
        
        user = User.query.filter(User.email=='janedoe@email.com').first()
        
        self.assertEquals(user.firstName, "Jane")
        self.assertEquals(user.lastName, "Doe")
        self.assertEquals(user.university, "UMBC")
        self.assertEquals(user.profile.year, None)
        self.assertEquals(user.profile.major, None)
        self.assertEquals(user.profile.biography, None)
        self.assertEquals(user.profile.classes, None)
        
        print '----------NEW USER2-----------'
        response = self.app.post('/deku/api/users', data = dict(
            firstName="John", lastName="Doe", email="johndoe@email.com",
                password='password', university="UMBC"))
        self.assertEquals(response.status_code, 201)
        print response.data
        
        user = User.query.filter(User.email=='johndoe@email.com').first()
        
        self.assertEquals(user.firstName, "John")
        self.assertEquals(user.lastName, "Doe")
        self.assertEquals(user.university, "UMBC")
        self.assertEquals(user.profile.year, None)
        self.assertEquals(user.profile.major, None)
        self.assertEquals(user.profile.biography, None)
        self.assertEquals(user.profile.classes, None)
        
        print '----------NEW USER3-----------'
        response = self.app.post('/deku/api/users', data = dict(
            firstName = "Carrie",
            lastName = "Hildebrand",
            email = 'carrie@carrie.com',
            password = 'password',
            university = "UMBC"))
        self.assertEquals(response.status_code, 201)
        print response.data
        
        user = User.query.filter(User.email=='carrie@carrie.com').first()
        
        self.assertEquals(user.firstName, "Carrie")
        self.assertEquals(user.lastName, "Hildebrand")
        self.assertEquals(user.university, "UMBC")
        self.assertEquals(user.profile.year, None)
        self.assertEquals(user.profile.major, None)
        self.assertEquals(user.profile.biography, None)
        self.assertEquals(user.profile.classes, None)
        
        print '----------NEW USER4-----------'
        
        response = self.app.post('/deku/api/users', data = dict(
            firstName = "Carrie",
            lastName = "Hildebrand",
            email = "carrie.hildebrand2@gmail.com",
            password = 'password',
            university = "UMBC",
            year = "yea",
            major ="major",
            classes="no classes!",
            biography="bio"))
        self.assertEquals(response.status_code, 201)
        print response.data
        
        user = User.query.filter(User.email=='carrie.hildebrand2@gmail.com').first()
        
        self.assertEquals(user.firstName, "Carrie")
        self.assertEquals(user.lastName, "Hildebrand")
        self.assertEquals(user.university, "UMBC")
        self.assertEquals(user.profile.year, "yea")
        self.assertEquals(user.profile.major, "major")
        self.assertEquals(user.profile.biography, "bio")
        self.assertEquals(user.profile.classes, "no classes!")
        
# Test user login
    #def test_user_login(self):
        print 'LOGIN--------'
        response = self.app.post('/deku/api/users/login', data = dict(email="johndoe@email.com",password="password"))
        print response.data
        self.assertEquals(response.status_code, 200)
        response=self.app.get('/deku/api/users/logged_in')
        self.assertEquals(response.status_code,200)
        
    #def test_user_login_bad_password(self):
        response = self.app.post('/deku/api/users/login', data = dict(
            email="johndoe@email.com",
            password="blahblahblah"))
        self.assertEquals(response.status_code, 401)
        response=self.app.get('/deku/api/users/logged_in')
        self.assertEquals(response.status_code,401)

    #def test_user_login_user_does_not_exist(self):
        response = self.app.post('/deku/api/users/login', data = dict(
            email="boristhesovietlovehammer@motherrussia.ru",
            password="putinismycomrade"))
        self.assertEquals(response.status_code, 404)
        response=self.app.get('/deku/api/users/logged_in')
        self.assertEquals(response.status_code,401)

        
        
# Test /deku/api/users POST
        print '----------modify info-----------'
        email='johndoe@email.com'
        password = 'fail'
        user = User.query.filter(User.email==email).first()
        temp = user.__dict__
        response = self.app.post('/deku/api/users/login', data = dict(
            email=email,
            password=password))
        print response.status_code
        response = self.app.put('/deku/api/users/'+str(temp['id']), data = dict(
            email=email,
            year = password))
        print response.status_code
        self.assertEquals(user.__dict__, temp)
        
        password = 'password'
        print '----------modify info-----------'
        response = self.app.post('/deku/api/users/login', data = dict(
            email=email,
            password='password'))
        response = self.app.put('/deku/api/users/'+str(temp['id']), data = dict(
            email='new email',
            year = 'year'))
        print response.status_code
        print response.data
        self.assertEquals(user.__dict__, temp)
        print '----------modify info-----------'

if __name__ == '__main__':

    unittest.main()