#!.venv/bin/python
import os
import unittest
import urllib2

from flask import json, jsonify
from config import basedir
from app import app, db, bcrypt, session
from app import users
from app import models
from app.models import User, Card
from sqlalchemy import outerjoin, desc

class APITestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()
       
        # from test_post_new_valid_user_with_no_profile 
        response = self.app.post('/deku/api/users', data=json.dumps(dict(firstName="Jane", lastName="Doe", email="janedoe@email.edu", password="jane", university="UMBC", grad_year="yea", major="major", classes=["no courses", "except this one","bbb"], bio="bio")),content_type='application/json')
        
        # from test_post_new_valid_user_with_full_profile
        response = self.app.post('/deku/api/users', data=json.dumps(dict(firstName="Carrie", lastName="Hildebrand", email="carrie@email.edu", password='carrie', university="UMBC", grad_year="yea", major="major", classes=["oneone", "two two"], bio="bio")),content_type='application/json')

        #admin
        response=self.app.post('/deku/api/users',data=json.dumps(dict(firstName="admin", lastName="admin", email="admin@deku.com", password="admin", university="admin",grad_year="admin", major="admin",classes=["admin"],bio="bio")),content_type='application/json')
#        self.assertEquals(response.headers['Access-Control-Allow-Origin'], "http://localhost:4567")
        user = models.User.query.filter(models.User.email=="admin@deku.com").first()
        user.role=models.ROLE_ADMIN
        db.session.commit()

        #from test_add_card_valid_min
  #      response = self.app.post('/deku/api/cards', data=json.dumps(dict(
  #                                                      user="janedoe@email.edu",
 #                                                       pwd="jane",
#                                                        content="cont",
#                                                        category="cat",
#                                                        tags=["one"])))
        
        
        #from test_add_card_valid_user_all
#        response = self.app.post('/deku/api/cards', data=dict(
#                                                              content="cont2",
#                                                              category="cat2",
#                                                              tags=['tag1','tag2']))
#        self.assertEquals(response.status_code,201)
        
#        response = self.app.post('/deku/api/users/login')
#        response = self.app.get('/deku/api/users/check_login')
#        self.assertEquals(response.status_code,401)
        
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def test_get_users(self):
        users = models.User.query.all()
        response = self.app.get('/deku/api/users')
        users=[user.serialize for user in users]
        self.assertEquals(json.loads(response.data)['users'],users)
        
    def test_get_user(self):
        user = models.User.query.filter(models.User.email=="carrie@email.edu").first()
        response = self.app.get('/deku/api/users/'+str(user.id))
        self.assertEquals(json.loads(response.data)['user'],user.serialize)

    def test_user_delete_and_post(self):
        id = models.User.query.filter(models.User.email=="janedoe@email.edu").first().id
        response = self.app.post('/deku/api/users', data=json.dumps(dict(firstName="Jane", lastName="Doe", email="janedoe@email.edu", password="jane", university="UMBC", grad_year="yea", major="major", classes=["no courses", "except this one","bbb"], bio="bio")),content_type='application/json')
        self.assertEquals(response.data,"Email already registered")
        #response = self.app.delete('/deku/api/users/'+str(id), data=json.dumps(dict(user="janedoe@email.edu",pwd="jane")),content_type='application/json')
        response = self.app.delete('/deku/api/users/'+str(id), data=json.dumps(dict(user="janedoe@email.edu",pwd="jane")),content_type='application/json')
        self.assertEquals(response.data,"User deleted")
        response = self.app.post('/deku/api/users', data=json.dumps(dict(firstName="Jane", lastName="Doe", email="janedoe@email.edu", password="jane", university="UMBC", grad_year="yea", major="major", classes=["no courses", "except this one","bbb"], bio="bio")),content_type='application/json')
        self.assertEquals(response.status_code,201)        
        
    
    def test_all_fields_user_post(self):
        user = models.User.query.filter(models.User.email=="janedoe@email.edu").first()
        self.assertEquals("Jane",user.firstName)
        self.assertEquals("Doe",user.lastName)
        self.assertEquals("janedoe@email.edu",user.email)
        self.assertTrue(bcrypt.check_password_hash(user.password,"jane"))
        self.assertEquals("UMBC",user.university)
        self.assertEquals("yea",user.profile.grad_year)
        self.assertEquals("major",user.profile.major)
        self.assertEquals("bio",user.profile.bio)
        self.assertEquals(len(user.profile.courses),3)
        
        
    def test_all_fields_user_put(self):
        id = models.User.query.filter(models.User.email=="carrie@email.edu").first().id
        response = self.app.put('/deku/api/users/'+str(id), data=json.dumps(dict(firstName="Jane", lastName="Doe", email="janedoee@email.edu", password="jane", university="UMBC", grad_year="yea", major="major", classes=["no courses", "except this one","bbb"], bio="bio")),content_type='application/json')
        user = models.User.query.filter(models.User.id==id).first()
        self.assertEquals("Jane",user.firstName)
        self.assertEquals("Doe",user.lastName)
        self.assertEquals("janedoee@email.edu",user.email)
        self.assertTrue(bcrypt.check_password_hash(user.password,"jane"))
        self.assertEquals("UMBC",user.university)
        self.assertEquals("yea",user.profile.grad_year)
        self.assertEquals("major",user.profile.major)
        self.assertEquals("bio",user.profile.bio)
        self.assertEquals(len(user.profile.courses),3)
        

if __name__ == '__main__':
    unittest.main()
