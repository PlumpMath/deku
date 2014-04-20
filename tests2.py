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
        
        
    def test_add_card_not_logged_in(self):
        response = self.app.post('/deku/api/cards', data=dict(
                                                              content="content"
                                                              ))
        self.assertEquals(response.status_code,401)
        
        
    def test_add_card_valid_user_minimum(self):
        #moved to setup
#        response = self.app.post('/deku/api/users/login',data=dict(email="janedoe@email.edu",password="password1"))
#        response = self.app.post('/deku/api/cards', data=dict(
#                                                              user="janedoe@email.edu",
#                                                              password="password1",
#                                                              content="cont",
#                                                             category="cat",
#                                                              tags=[]
#                                                              ))
#        self.assertEquals(response.status_code,201)
        response = self.app.post('/deku/api/users/login',data=dict(email="janedoe@email.edu",password="password1"))
        id = models.User.query.filter(models.User.email=='janedoe@email.edu').first().id
        card = models.Card.query.filter(models.Card.id==id).first()
        self.assertEquals(card.content,"cont")
        self.assertEquals(card.category,"cat")
        self.assertEquals(len(card.tags),0)

        
        
    def test_add_card_valid_user_all(self):
        #moved to setup
#        response = self.app.post('/deku/api/users/login',data=dict(email="janedoe@email.edu",password="password1"))
#        response = self.app.post('/deku/api/cards', data=dict(
#                                                              user="janedoe@email.edu",
#                                                              password="password1",
#                                                              content="cont2",
#                                                              category="cat2",
#                                                              tags=['tag1','tag2']
#                                                              ))
#        self.assertEquals(response.status_code,201)
        response = self.app.post('/deku/api/users/login',data=dict(email="janedoe@email.edu",password="jane"))
        id = models.User.query.filter(models.User.email=='janedoe@email.edu').first().id
        card = models.Card.query.filter(models.Card.user_id==id).order_by(desc(models.Card.id)).first()
        
        self.assertEquals(card.content,"cont2")
        self.assertEquals(card.category,"cat2")
        self.assertEquals(len(card.tags),2)
        tags = models.Tag.query.filter(models.Tag.tag=='tag1').filter(models.User.id==id).all()
        self.assertEquals(len(tags),1)
        tags = models.Tag.query.filter(models.Tag.tag=='tag2').filter(models.User.id==id).all()
        self.assertEquals(len(tags),1)
        
    def test_mod_content_wrong_user(self):
        response = self.app.post('/deku/api/users/login',data=dict(email="carrie.hildebrand2@gmail.com",password="carrie"))
        id = db.session.query(models.User).filter(models.User.email=="janedoe@email.edu").first().id
        self.assertEquals(response.status_code,200)
        card = db.session.query(models.Card).filter(models.Card.user_id==id).first()
        before = card.serialize
        response = self.app.put('/deku/api/cards/'+str(card.id),data=dict(content="something"))
        self.assertEquals(response.data,"Invalid Request")
        self.assertEquals(response.status_code,400)
        card = db.session.query(models.Card).filter(models.Card.user_id==id).first()
        after = card.serialize
        self.assertEquals(before,after)
        
    def test_mod_content_not_logged_in(self):
        #logout
        response = self.app.post('/deku/api/users/login')
        id = db.session.query(models.User).filter(models.User.email=="janedoe@email.edu").first().id
        self.assertEquals(response.status_code,401)
        card = db.session.query(models.Card).filter(models.Card.user_id==id).first()
        before = card.serialize
        response = self.app.put('/deku/api/cards/'+str(card.id),data=dict(content="something"))
        card = db.session.query(models.Card).filter(models.Card.user_id==id).first()
        after = card.serialize
        self.assertEquals(before,after)
        
        
    def test_mod_content_success(self):
        response = self.app.post('/deku/api/users/login',data=dict(email="janedoe@email.edu",password="jane"))
        id = db.session.query(models.User).filter(models.User.email=="janedoe@email.edu").first().id
        self.assertEquals(response.status_code,200)
        card = db.session.query(models.Card).filter(models.Card.user_id==id).first()
        print card
        before = card.serialize
        response = self.app.put('/deku/api/cards/'+str(card.id),data=dict(content="something"))
        card = db.session.query(models.Card).filter(models.Card.user_id==id).first()
        print card
        after = card.serialize
        self.assertNotEquals(before,after)

    def test_mod_content_invalid_card(self):
        response = self.app.post('/deku/api/users/login',data=dict(email="janedoe@email.edu",password="jane"))
        self.assertEquals(response.status_code,200)
        response = self.app.put('/deku/api/cards/9999',data=dict(content="something"))
        self.assertEquals(response.status_code,400)
        self.assertEquals(response.data,"Invalid Request 1",400)


        
    def test_delete_card_unauth(self):
        user = models.User.query.filter(models.User.email=="janedoe@email.edu").first()
        cards = models.Card.query.filter(models.Card.user_id==user.id).all()
        num = len(cards)
        for card in cards:
            response = self.app.delete('/deku/api/cards/'+str(card.id))
            self.assertEquals(response.data,"Unauthorized Access")
            self.assertEquals(response.status_code,401)
        cards = models.Card.query.filter(models.Card.user_id==user.id).all()
        self.assertEquals(num,len(cards))
        
    def test_delete_card_does_not_exist(self):
        self.app.post('/deku/api/users/login',data=dict(email="janedoe@email.edu",password='jane'))
        print '-------------------'
        response = self.app.delete('/deku/api/cards/9999',data=dict(user="carrie.hildebrand2@gmail.com",pwd="password"))
        self.assertEquals(response.data,"Invalid request")
    
    def test_delete_card_bad_user(self):
        self.app.post('/deku/api/users/login',data=dict(email="carrie.hildebrand2@gmail.com",password='carrie'))
        user = models.User.query.filter(models.User.email=="janedoe@email.edu").first()
        cards = models.Card.query.filter(models.Card.user_id==user.id).all()
        for card in cards:
            response = self.app.open('/deku/api/cards/'+str(card.id),method="DELETE",data=dict(user="carrie.hildebrand2@gmail.com",pwd="password"))
            self.assertEquals(response.data,"Invalid request 1")
            self.assertEquals(response.status_code,400)
            
    def test_delete_card_not_logged_in(self):
        #self.app.post('/deku/api/users/login',data=dict(email="carrie.hildebrand2@gmail.com",password="carrie"))
        response = self.app.delete('/deku/api/cards/1')
        self.assertEquals(response.data,"Unauthorized Access")
        cards=models.Card.query.filter(models.Card.id==1).all()
        self.assertEquals(len(cards),1)
        
    def test_delete_card_valid(self):
        card = models.Card.query.filter(models.Card.id==1).first()
        self.app.post('/deku/api/users/login',data=dict(email=card.author.email,password='jane'))
        result = self.app.get('/deku/api/users/check_login')
        self.assertEquals(result.data,"good")
        response = self.app.delete('/deku/api/cards/1')
        self.assertEquals(response.data,"Card deleted.")
        cards=models.Card.query.filter(models.Card.id==1).all()
        self.assertEquals(len(cards),0)
        

        
#CASCADING DELETES CHECKED AT END OF TESTS.PY


if __name__ == '__main__':
    unittest.main()



