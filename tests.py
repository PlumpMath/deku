#!.venv/bin/python
import os
import unittest
import urllib2

from flask import json
from config import basedir
from app import app, db, bcrypt, session, models
from app.models import User, Card
from sqlalchemy import outerjoin

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
        
        #add first new user
        print '----------NEW USER1-----------'
        response = self.app.post('/deku/api/users', data = dict(firstName="Jane", lastName="Doe", email="janedoe@email.com", password="password1", university="UMBC"))
        self.assertEquals(response.status_code, 201)
        print response.data
        
        user = User.query.filter(User.email=='janedoe@email.com').first()
        self.assertEquals(user.firstName, "Jane")
        self.assertEquals(user.lastName, "Doe")
        self.assertEquals(user.university, "UMBC")
        self.assertEquals(user.profile.grad_year, None)
        self.assertEquals(user.profile.major, None)
        self.assertEquals(user.profile.bio, None)
        self.assertEquals(len(user.profile.courses), 0)
        
        
        #add second new user
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
        self.assertEquals(user.profile.grad_year, None)
        self.assertEquals(user.profile.major, None)
        self.assertEquals(user.profile.bio, None)
        self.assertEquals(len(user.profile.courses), 0)
        
        
        #add third new user
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
        self.assertEquals(user.profile.grad_year, None)
        self.assertEquals(user.profile.major, None)
        self.assertEquals(user.profile.bio, None)
        self.assertEquals(len(user.profile.courses), 0)
        
        
        #add fourth new user
        print '----------NEW USER4-----------'
        
        response = self.app.post('/deku/api/users', data = dict(
            firstName = "Carrie",
            lastName = "Hildebrand",
            email = "carrie.hildebrand2@gmail.com",
            password = 'password',
            university = "UMBC",
            grad_year = "yea",
            major ="major",
            classes=["no courses!","except this one"],
            bio="bio"))
        self.assertEquals(response.status_code, 201)
        print response.data
        
        user = User.query.filter(User.email=='carrie.hildebrand2@gmail.com').first()
        
        self.assertEquals(user.firstName, "Carrie")
        self.assertEquals(user.lastName, "Hildebrand")
        self.assertEquals(user.university, "UMBC")
        self.assertEquals(user.profile.grad_year, "yea")
        self.assertEquals(user.profile.major, "major")
        self.assertEquals(user.profile.bio, "bio")

        course = db.session.query(models.Course, models.User).outerjoin(models.User, models.User.id==models.Course.user_id).filter(models.Course.course=="except this one").first()
        self.assertEquals(course[0].course, "except this one")
        self.assertEquals(course[1].firstName, "Carrie")

        course = db.session.query(models.Course, models.User).outerjoin(models.User, models.User.id==models.Course.user_id).filter(models.Course.course=="no courses!").first()
        self.assertEquals(course[0].course, "no courses!")
        self.assertEquals(course[1].firstName, "Carrie")

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
        #failure to modify email because not logged in
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
            grad_year = password))
        print response.status_code
        self.assertEquals(user.__dict__, temp)
        
        password = 'password'
        print '----------modify info-----------'
        #success modifying info
        response = self.app.post('/deku/api/users/login', data = dict(
            email=email,
            password='password'))
        response = self.app.put('/deku/api/users/'+str(temp['id']), data = dict(
            email='new email',
            grad_year = 'year'))
        print response.status_code
        print response.data
        user = db.session.query(models.User, models.Profile).outerjoin(models.Profile,models.User.id==models.Profile.user_id).filter(models.User.id==str(temp['id'])).first()
        self.assertEquals(user[0].firstName,"John")
        self.assertEquals(user[0].email, "new email")
        self.assertEquals(user[1].grad_year, "year")
        
        
        #setting (not appending) 3 courses
        response = self.app.put('/deku/api/users/'+str(temp['id']), data = dict(
            classes=['new email','two','three']))
        response = self.app.put('/deku/api/users/'+str(temp['id']), data = dict(
            classes=['new email','two','three']))
        print response.status_code
        print response.data
        
        
        #John is the first person to take new email
        course = db.session.query(models.Course,models.User).outerjoin(models.User,models.Course.user_id==models.User.id).filter(models.Course.course=="new email").first()
        self.assertEquals(course[1].firstName,"John")
        #John is the first person to take two
        course = db.session.query(models.Course,models.User).outerjoin(models.User,models.Course.user_id==models.User.id).filter(models.Course.course=="two").first()
        self.assertEquals(course[1].firstName,"John")
        #John is the first person to take three
        course = db.session.query(models.Course,models.User).outerjoin(models.User,models.Course.user_id==models.User.id).filter(models.Course.course=="three").first()
        self.assertEquals(course[1].firstName,"John")
        #There is only one person taking new email
        course = db.session.query(models.Course,models.User).outerjoin(models.User,models.Course.user_id==models.User.id).filter(models.Course.course=="new email").all()
        self.assertEquals(len(course),1)
        
        
        #Test Add Card
        print '----------login-----------'
        response = self.app.post('/deku/api/users/login', data = dict(
            email='janedoe@email.com',
            password='password1'))
        data = json.loads(response.data)
        id = data['user']['id']
        print response.status_code
        print '----------add card-----------'
        tags=json.dumps(['one','two','three'])
        print tags
        response = self.app.post('/deku/api/cards', data=dict(
            content='some other content',
            tags=tags,
            suit='someothersuit'))
        print response.data
        
        print '----------add another card-----------'
        tags=json.dumps(['tag','ta'])
        print tags
        response = self.app.post('/deku/api/cards', data=dict(
            content='some content',
            tags=tags,
            suit='somesuit'))
        print response.data
        
        print '-----------get all cards-----'
        response = self.app.get('/deku/api/cards', data=dict())
        data = response.data
        data = json.loads(data)
        print data['cards']
        self.assertEquals(len(data['cards']),2)
        
        print '----------get 1st card-------'    
        response = self.app.get('/deku/api/cards/1', data=dict())
        data = json.loads(response.data)
        self.assertEquals(len(data['card']['tags'].split(",")),3)
        
        print '----------get 2nd card-------'    
        response = self.app.get('/deku/api/cards/2', data=dict())
        data = json.loads(response.data)
        self.assertEquals(len(data['card']['tags'].split(",")),2)


        
if __name__ == '__main__':
    unittest.main()
