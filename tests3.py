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
from sqlalchemy import outerjoin, desc

class APITestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()
       
        # from test_post_new_valid_user_with_no_profile
        response = self.app.post('/deku/api/users', data=dict(firstName="Jane", lastName="Doe", email="janedoe@email.edu", password="jane", university="UMBC"))
        self.assertEquals(response.headers['Access-Control-Allow-Origin'], "http://localhost:4567")
        
        
        # from test_post_new_valid_user_with_full_profile
        response = self.app.post('/deku/api/users', data=dict(firstName="Carrie", lastName="Hildebrand", email="carrie.hildebrand2@gmail.com", password='carrie', university="UMBC", grad_year="yea", major="major", classes=["no courses", "except this one","bbb"], bio="bio"))
        self.assertEquals(response.headers['Access-Control-Allow-Origin'], "http://localhost:4567")

        #admin        
        response=self.app.post('/deku/api/users',data=dict(firstName="admin", lastName="admin", email="admin@deku.com", university="admin", password="admin"))
        self.assertEquals(response.headers['Access-Control-Allow-Origin'], "http://localhost:4567")
        user = models.User.query.filter(models.User.email=="admin@deku.com").first()
        user.role=models.ROLE_ADMIN
        db.session.commit()



        
        #from test_add_card_valid_min
        response = self.app.post('/deku/api/users/login',data=dict(email="janedoe@email.edu",password="jane"))
        response = self.app.post('/deku/api/cards', data=dict(
                                                              content="cont",
                                                             category="cat",
                                                              tags=[]
                                                              ))
        self.assertEquals(response.status_code,201)
        
        
        #from test_add_card_valid_user_all
        response = self.app.post('/deku/api/cards', data=dict(
                                                              content="cont2",
                                                              category="cat2",
                                                              tags=['tag1','tag2']))
        self.assertEquals(response.status_code,201)
        
        response = self.app.post('/deku/api/users/login')
        response = self.app.get('/deku/api/users/check_login')
        self.assertEquals(response.status_code,401)
        
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def test_add_comments_success(self):
        #add to card1
        response = self.app.post('/deku/api/users/login',data=dict(email="janedoe@email.edu",password="jane"))
        data = json.loads(response.data)
        id = data['user'].get('id')
        response = self.app.post('/deku/api/cards/comment/1',data=dict(comment="a comment"))
        self.assertEquals(response.status_code,201)
        comment = db.session.query(models.Comment).filter(models.Comment.user_id==id).filter(models.Comment.comment=="a comment").first()
        self.assertEquals(comment.comment,"a comment")

        response = self.app.post('/deku/api/cards/comment/1',data=dict(comment="another comment"))
        self.assertEquals(response.status_code,201)
        comments = db.session.query(models.Comment).filter(models.Comment.card_id==1).all()
        self.assertEquals(len(comments),2)
        for comment in comments:
            print comment.serialize


if __name__ == '__main__':
    unittest.main()



