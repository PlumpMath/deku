#!.venv/bin/python
import os
import unittest
import urllib2

from flask import json
from config import basedir
from app import app, db, bcrypt, session, models, users
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
        response = self.app.post('/deku/api/cards', data=dict(
                                                              user="janedoe@email.edu",
                                                              password="password1",
                                                              content="cont",
                                                             category="cat",
                                                              tags=[]
                                                              ))
        self.assertEquals(response.status_code,201)
        
        
        #from test_add_card_valid_user_all
        response = self.app.post('/deku/api/cards', data=dict(
                                                              user="janedoe@email.edu",
                                                              password="password1",
                                                              content="cont2",
                                                              category="cat2",
                                                              tags=['tag1','tag2']))
        self.assertEquals(response.status_code,201)
        
          
        
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
        
    def test_add_card_invalid_user(self):
        response = self.app.post('/deku/api/cards', data=dict(
                                                              user="something",
                                                              password="wrong"
                                                              ))
        self.assertEquals(response.status_code,401)
        
        
    def test_add_card_valid_user_minimum(self):
#        response = self.app.post('/deku/api/cards', data=dict(
#                                                              user="janedoe@email.edu",
#                                                              password="password1",
#                                                              content="cont",
#                                                             category="cat",
#                                                              tags=[]
#                                                              ))
#        self.assertEquals(response.status_code,201)
        id = models.User.query.filter(models.User.email=='janedoe@email.edu').first().id
        card = models.Card.query.filter(models.Card.id==id).first()
        self.assertEquals(card.content,"cont")
        self.assertEquals(card.category,"cat")
        self.assertEquals(len(card.tags),0)

        
        
    def test_add_card_valid_user_all(self):
#        response = self.app.post('/deku/api/cards', data=dict(
#                                                              user="janedoe@email.edu",
#                                                              password="password1",
#                                                              content="cont2",
#                                                              category="cat2",
#                                                              tags=['tag1','tag2']
#                                                              ))
#        self.assertEquals(response.status_code,201)
        id = models.User.query.filter(models.User.email=='janedoe@email.edu').first().id
        card = models.Card.query.filter(models.Card.user_id==id).order_by(desc(models.Card.id)).first()
        
        self.assertEquals(card.content,"cont2")
        self.assertEquals(card.category,"cat2")
        self.assertEquals(len(card.tags),2)
        tags = models.Tag.query.filter(models.Tag.tag=='tag1').filter(models.User.id==id).all()
        self.assertEquals(len(tags),1)
        tags = models.Tag.query.filter(models.Tag.tag=='tag2').filter(models.User.id==id).all()
        self.assertEquals(len(tags),1)

    def test_get_all_cards(self):
        response = self.app.get('/deku/api/cards')
        data = json.loads(response.data)
        print len(data['cards'])
        self.assertEquals(len(data['cards']),2)
        

if __name__ == '__main__':
    unittest.main()
