#!.venv/bin/python
import os
import unittest
import urllib2

from flask import json
from config import basedir
from app import app, db, bcrypt, session
from app import users
from app import models
from app.models import User, Card
from app.users import authenticate
from sqlalchemy import outerjoin

class APITestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()
       
        # from test_post_new_valid_user_with_no_profile
        response = self.app.post('/deku/api/users', data=dict(firstName="Jane", lastName="Doe", email="janedoe@email.edu", password="password1", university="UMBC"))
        self.assertEquals(response.headers['Access-Control-Allow-Origin'], "http://localhost:4567")
        
        
        # from test_post_new_valid_user_with_full_profile
        response = self.app.post('/deku/api/users', data=dict(firstName="Carrie", lastName="Hildebrand", email="carrie.hildebrand2@gmail.com", password='password', university="UMBC", grad_year="yea", major="major", classes=["no courses", "except this one","bbb"], bio="bio"))
        self.assertEquals(response.headers['Access-Control-Allow-Origin'], "http://localhost:4567")

        #admin        
        response=self.app.post('/deku/api/users',data=dict(firstName="admin", lastName="admin", email="admin@deku.com", university="admin", password="admin"))
        self.assertEquals(response.headers['Access-Control-Allow-Origin'], "http://localhost:4567")
        user = models.User.query.filter(models.User.email=="admin@deku.com").first()
        user.role=models.ROLE_ADMIN
        db.session.commit()
        
        #from test_add_card_valid_min
        response = self.app.post('/deku/api/users/login',data=dict(email="janedoe@email.edu",password="password1"))
        response = self.app.post('/deku/api/cards', data=dict(
                                                              content="cont",
                                                             category="cat",
                                                              tags=[]
                                                              ))
        self.assertEquals(response.status_code,201)
        
        
        #from test_add_card_valid_user_all
        response = self.app.post('/deku/api/users/login',data=dict(email="janedoe@email.edu",password="password1"))
        response = self.app.post('/deku/api/cards', data=dict(
                                                              content="cont2",
                                                              category="cat2",
                                                              tags=['tag1','tag2']))
        self.assertEquals(response.status_code,201)
        
        response = self.app.put('/deku/api/users/logout',data=dict(email="janedoe@email.edu",password="password1"))
        response = self.app.get('/deku/api/users/check_login')
        self.assertEquals(response.status_code,401)
        
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
        
    def test_login_fail(self):
        response = self.app.post('/deku/api/users/login',data=dict(email="cArrie.hildebrand2@gmail.com",password="pAssword"))
        self.assertEquals(response.status_code,401)
        response = self.app.open('/deku/api/users/check_login', method='GET')
        self.assertEquals(response.status_code,401)
        
    def test_login_success(self):
        response = self.app.post('/deku/api/users/login',data=dict(email="caRRie.hildebrand2@gmail.com",password="password"))
        self.assertEquals(response.status_code,200)
        response = self.app.open('/deku/api/users/check_login', method='GET')
        self.assertEquals(response.status_code,200)
        
    def test_logout(self):
        response = self.app.post('/deku/api/users/login',data=dict(email="caRRie.hildebrand2@gmail.com",password="password"))
        self.assertEquals(response.status_code,200)
        response = self.app.put('/deku/api/users/logout',data=dict(email="janedoe@email.edu",password="password1"))
        response = self.app.get('/deku/api/users/check_login')
        self.assertEquals(response.status_code,401)

    # this works so the first two lines are commented out because it has been moved to setup
    # register a new user without profile
    def test_post_new_valid_user_with_no_profile(self):
        # response = self.app.post('/deku/api/users', data = dict(firstName="Jane", lastName="Doe", email="janedoe@email.edu", password="password1", university="UMBC"))
        # self.assertEquals(response.status_code, 201)
        user = User.query.filter(User.email == "janedoe@email.edu").first()
        self.assertEquals(user.firstName, "Jane")
        self.assertEquals(user.lastName, "Doe")
        self.assertEquals(user.university, "UMBC")
        self.assertEquals(user.email, "janedoe@email.edu")
        self.assertEquals(user.profile.grad_year, None)
        self.assertEquals(user.profile.major, None)
        self.assertEquals(user.profile.bio, None)
        self.assertTrue(bcrypt.check_password_hash(user.password, "password1"))
        self.assertEquals(len(user.profile.courses), 0)


    # this works so the first two lines are commented out because it has been moved to setup
    # register a new user with profile and classes
    def test_post_new_valid_user_with_full_profile(self):
#        response = self.app.post('/deku/api/users', data = dict(
#            firstName = "Carrie",
#            lastName = "Hildebrand",
#            email = "carrie.hildebrand2@gmail.com",
#            password = 'password',
#            university = "UMBC",
#            grad_year = "yea",
#            major ="major",
#            classes=["no courses","except this one"],
#            bio="bio"))
#        self.assertEquals(response.status_code, 201)
        user = User.query.filter(User.email == 'carrie.hildebrand2@gmail.com').first()
        
        self.assertEquals(user.firstName, "Carrie")
        self.assertEquals(user.lastName, "Hildebrand")
        self.assertEquals(user.university, "UMBC")
        self.assertEquals(user.email, "carrie.hildebrand2@gmail.com")
        self.assertEquals(user.profile.grad_year, "yea")
        self.assertEquals(user.profile.major, "major")
        self.assertEquals(user.profile.bio, "bio")
        self.assertTrue(bcrypt.check_password_hash(user.password, "password"))

        course = db.session.query(models.Course, models.User).outerjoin(models.User, models.User.id == models.Course.user_id).filter(models.Course.course == "except this one").first()
        self.assertEquals(course[0].course, "except this one")
        self.assertEquals(course[1].firstName, "Carrie")

        course = db.session.query(models.Course, models.User).outerjoin(models.User, models.User.id == models.Course.user_id).filter(models.Course.course == "no courses").first()
        self.assertEquals(course[0].course, "no courses")
        self.assertEquals(course[1].firstName, "Carrie")
        
        course = db.session.query(models.Course, models.User).outerjoin(models.User, models.User.id == models.Course.user_id).filter(models.Course.course == "bbb").first()
        self.assertEquals(course[0].course, "bbb")
        self.assertEquals(course[1].firstName, "Carrie")
        
    def test_modify_own_user_fields(self):
        response = self.app.post('/deku/api/users/login',data=dict(email="caRRie.hildebrand2@gmail.com",password="password"))
        response = self.app.open('/deku/api/users/check_login', method='GET')
        self.assertEquals(response.status_code,200)
        # change all of carrie's fields to "a"
        user = User.query.filter(User.email == 'carrie.hildebrand2@gmail.com').first()
        before = "" + str(user.serialize) + user.password

        
        # user and pwd are used to confirm authentication.  email and password are for changing email and password
        response = self.app.put('/deku/api/users/' + str(user.id), data=dict(firstName="a", lastName="b", university="c", email="d", password="h", grad_year="e", major="f", bio="g", classes=["aaa", "bbb", "ccc", "ddd"]))
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.headers['Access-Control-Allow-Origin'], "http://localhost:4567")

        user = User.query.filter(User.email == 'carrie.hildebrand2@gmail.com').all()
        self.assertEquals(len(user), 0)
        user = User.query.filter(User.email == 'd').first()        
        self.assertEquals(user.firstName, "a")
        self.assertEquals(user.lastName, "b")
        self.assertEquals(user.university, "c")
        self.assertEquals(user.email, "d")
        self.assertEquals(user.profile.grad_year, "e")
        self.assertEquals(user.profile.major, "f")
        self.assertEquals(user.profile.bio, "g")
        self.assertTrue(bcrypt.check_password_hash(user.password, "h"))
        
        courses = models.Course.query.filter(User.id == user.id).all()
        self.assertEquals(len(courses), 4)
        course = models.Course.query.filter(User.id == user.id).filter(models.Course.course == "aaa").all()
        self.assertEquals(len(course), 1)
        course = models.Course.query.filter(User.id == user.id).filter(models.Course.course == "bbb").all()
        self.assertEquals(len(course), 1)
        course = models.Course.query.filter(User.id == user.id).filter(models.Course.course == "ccc").all()
        self.assertEquals(len(course), 1)
        course = models.Course.query.filter(User.id == user.id).filter(models.Course.course == "ddd").all()
        self.assertEquals(len(course), 1)
        after = "" + str(user.serialize) + user.password
        self.assertNotEqual(before, after)

        
        
    def test_unauthenticated_modify_user_fields(self):
        # change all of carrie's fields to "a"
        user = User.query.filter(User.email == 'carrie.hildebrand2@gmail.com').first()
        before = "" + str(user.serialize) + user.password
        
        # user and pwd are used to confirm authentication.  email and password are for changing email and password
        response = self.app.put('/deku/api/users/' + str(user.id), data=dict(firstName="a", lastName="b", university="c", email="d", password="h", grad_year="e", major="f", bio="g", classes=["aaa", "bbb", "ccc", "ddd"]))
        self.assertEquals(response.status_code, 401)
        self.assertEquals(response.headers['Access-Control-Allow-Origin'], "http://localhost:4567")

        user = User.query.filter(User.email == 'carrie.hildebrand2@gmail.com').first()        
        
        after = "" + str(user.serialize) + user.password
        self.assertEquals(before, after)
        
        
    def test_modify_other_user_fields_non_admin(self):
        response = self.app.post('/deku/api/users/login',data=dict(email="janedoe@email.edu",password="password1"))
        # change all of carrie's fields to "a"
        user = User.query.filter(User.email == 'carrie.hildebrand2@gmail.com').first()
        before = "" + str(user.serialize) + user.password
        # user and pwd are used to confirm authentication.  email and password are for changing email and password
        response = self.app.put('/deku/api/users/' + str(user.id), data=dict(firstName="a", lastName="b", university="c", email="d", password="h", grad_year="e", major="f", bio="g", classes=["aaa", "bbb", "ccc", "ddd"]))
        self.assertEquals(response.headers['Access-Control-Allow-Origin'], "http://localhost:4567")
        self.assertEquals(response.data, "Unauthorized Access 1")

        user = User.query.filter(User.email == 'carrie.hildebrand2@gmail.com').first()
        
        after = "" + str(user.serialize) + user.password
        self.assertEquals(before, after)
        
        
    def test_modify_other_user_fields_as_admin(self):
        response = self.app.post('/deku/api/users/login',data=dict(email="admin@deku.com", password="admin"))
        response = self.app.post('/deku/api/users/check_login')
        # change all of carrie's fields to "a"
        user = User.query.filter(User.email == 'carrie.hildebrand2@gmail.com').first()
        before = "" + str(user.serialize) + user.password
        # user and pwd are used to confirm authentication.  email and password are for changing email and password
        response = self.app.put('/deku/api/users/' + str(user.id), data=dict(firstName="a", lastName="b", university="c", email="d", password="h", grad_year="e", major="f", bio="g", classes=["aaa", "bbb", "ccc", "ddd"]))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.headers['Access-Control-Allow-Origin'], "http://localhost:4567")

        user = User.query.filter(User.email == 'carrie.hildebrand2@gmail.com').all()
        self.assertEquals(len(user), 0)
        user = User.query.filter(User.email == 'd').first()      
        self.assertEquals(user.firstName, "a")
        self.assertEquals(user.lastName, "b")
        self.assertEquals(user.university, "c")
        self.assertEquals(user.email, "d")
        self.assertEquals(user.profile.grad_year, "e")
        self.assertEquals(user.profile.major, "f")
        self.assertEquals(user.profile.bio, "g")
        self.assertTrue(bcrypt.check_password_hash(user.password, "h"))
        
        courses = models.Course.query.filter(User.id == user.id).all()
        self.assertEquals(len(courses), 4)
        course = models.Course.query.filter(User.id == user.id).filter(models.Course.course == "aaa").all()
        self.assertEquals(len(course), 1)
        course = models.Course.query.filter(User.id == user.id).filter(models.Course.course == "bbb").all()
        self.assertEquals(len(course), 1)
        course = models.Course.query.filter(User.id == user.id).filter(models.Course.course == "ccc").all()
        self.assertEquals(len(course), 1)
        course = models.Course.query.filter(User.id == user.id).filter(models.Course.course == "ddd").all()
        self.assertEquals(len(course), 1)
        after = "" + str(user.serialize) + user.password
        self.assertNotEqual(before, after)
        

    def test_get_valid_user_by_id(self):
        user = User.query.filter(User.email == 'carrie.hildebrand2@gmail.com').first() 
        before = user.serialize
        response = self.app.get('/deku/api/users/' + str(user.id))
        self.assertEquals(response.headers['Access-Control-Allow-Origin'], "http://localhost:4567")
        data = json.loads(response.data)
        self.assertEquals(response.status_code,200)
        self.assertEquals(data['user'], before)

    def test_get_invalid_user_by_id(self):
        user = User.query.filter(User.email == 'carrie.hildebrand2@gmail.com').first() 
        response = self.app.get('/deku/api/users/' + str(user.id))
        self.assertEquals(response.headers['Access-Control-Allow-Origin'], "http://localhost:4567")
        self.assertEquals(response.status_code,200)
        
    def test_get_all_users(self):
        response = self.app.get('/deku/api/users')
        self.assertEquals(response.headers['Access-Control-Allow-Origin'], "http://localhost:4567")
        data = json.loads(response.data)
        self.assertEquals(response.status_code,200)
        self.assertEquals(len(User.query.all()),len(data['users']))
        for user in data['users']:
            check_user = User.query.filter(User.email==user['email']).first()
            self.assertEquals(check_user.serialize,user)
        
    def test_delete_self(self):
        response = self.app.post('/deku/api/users/login',data=dict(email="janedoe@email.edu",password="password1"))
        data = json.loads(response.data)
        id = data['user']['id']
        user = models.User.query.filter(models.User.id==id).first()
        tags=[]
        for card in user.cards:
            for tag in card.tags:
                tags.append(tag.id)
        self.assertEquals(response.status_code,200)
        response = self.app.delete('/deku/api/users/'+str(id))
        users = models.User.query.filter(models.User.id==id).all()
        self.assertEquals(len(users),0)
        cards = models.Card.query.filter(models.Card.user_id==id).all()
        self.assertEquals(len(cards),0)
        for tag in tags:
            tags = models.Tag.query.filter(models.Tag.id==tag).all()
            self.assertEquals(len(tags),0)
        profiles = models.Profile.query.filter(models.Profile.user_id==id).all()
        self.assertEquals(len(profiles),0)
        comments = models.Comment.query.filter(models.Comment.user_id==id).all()
        self.assertEquals(len(comments),0)
        
    def test_delete_not_logged_in(self):
        id = models.User.query.filter(models.User.email=="carrie.hildebrand2@gmail.com").first().id
        print id
        response = self.app.delete('/deku/api/users/'+str(id))
        self.assertEquals(response.data,"Unauthorized Access")
        
    def test_delete_other_as_non_admin(self):
        response = self.app.post('/deku/api/users/login',data=dict(email="janedoe@email.edu",password="password1"))
        id = models.User.query.filter(models.User.email=="carrie.hildebrand2@gmail.com").first().id
        response = self.app.delete('/deku/api/users/'+str(id))
        self.assertEquals(response.data,"Unauthorized Access 1")
        
    def test_delete_other_as_admin(self):
        response = self.app.post('/deku/api/users/login',data=dict(email="admin@deku.com",password="admin"))
        data = json.loads(response.data)
        id = data['user']['id']
        user = models.User.query.filter(models.User.id==id).first()
        tags=[]
        for card in user.cards:
            for tag in card.tags:
                tags.append(tag.id)
        self.assertEquals(response.status_code,200)
        response = self.app.delete('/deku/api/users/'+str(id))
        users = models.User.query.filter(models.User.id==id).all()
        self.assertEquals(len(users),0)
        cards = models.Card.query.filter(models.Card.user_id==id).all()
        self.assertEquals(len(cards),0)
        for tag in tags:
            tags = models.Tag.query.filter(models.Tag.id==tag).all()
            self.assertEquals(len(tags),0)
        profiles = models.Profile.query.filter(models.Profile.user_id==id).all()
        self.assertEquals(len(profiles),0)
        comments = models.Comment.query.filter(models.Comment.user_id==id).all()
        self.assertEquals(len(comments),0)
        
if __name__ == '__main__':
    unittest.main()
