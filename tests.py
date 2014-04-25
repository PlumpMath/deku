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
        response = self.app.post('/deku/api/users', data=dict(firstName="Jane", lastName="Doe", email="janedoe@email.edu", password="jane", university="UMBC", grad_year="yea", major="major", classes=["no courses", "except this one","bbb"], bio="bio"))
        
        # from test_post_new_valid_user_with_full_profile
        response = self.app.post('/deku/api/users', data=dict(firstName="Carrie", lastName="Hildebrand", email="carrie@email.edu", password='carrie', university="UMBC", grad_year="yea", major="major", classes=["oneone", "two two"], bio="bio"))

        #admin
        response=self.app.post('/deku/api/users',data=dict(firstName="admin", lastName="admin", email="admin@deku.com", password="admin", university="admin",grad_year="admin", major="admin",classes=["admin"],bio="bio"))
#        self.assertEquals(response.headers['Access-Control-Allow-Origin'], "http://localhost:4567")
        user = models.User.query.filter(models.User.email=="admin@deku.com").first()

        user.role=models.ROLE_ADMIN
        db.session.commit()

        #from test_add_card_valid_min
        response = self.app.post('/deku/api/cards', data=dict(
                                                        user="janedoe@email.edu",
                                                        pwd="jane",
                                                        content="content1",
                                                        category="cat",
                                                        tags=["one","two"],
                                                        comments=['','comment 2','comment 3']))
        
        
        response = self.app.post('/deku/api/cards', data=dict(
                                                        user="janedoe@email.edu",
                                                        pwd="jane",
                                                        content="content2",
                                                        category="cat",
                                                        tags=["one"]))

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def test_get_users(self):
        users = models.User.query.order_by(models.User.id.desc()).all()
        response = self.app.get('/deku/api/users')
        users=[user.serialize for user in users]
        self.assertEquals(json.loads(response.data)['users'],users)
        
    def test_get_user(self):
        user = models.User.query.filter(models.User.email=="carrie@email.edu").first()
        response = self.app.get('/deku/api/users/'+str(user.id))
        self.assertEquals(json.loads(response.data)['user'],user.serialize)

    def test_user_delete(self):
        id = models.User.query.filter(models.User.email=="janedoe@email.edu").first().id
        #make sure its there
        response = self.app.post('/deku/api/users', data=dict(firstName="Jane", lastName="Doe", email="janedoe@email.edu", password="jane", university="UMBC", grad_year="yea", major="major", classes=["no courses", "except this one","bbb"], bio="bio"))
        self.assertEquals(response.data,"Email already registered")
        #delete
        response = self.app.post('/deku/api/users/delete/'+str(id), data=dict(user="janedoe@email.edu",pwd="jane"))
        self.assertEquals(response.data,"User deleted")
        #add
        response = self.app.post('/deku/api/users', data=dict(firstName="Jane", lastName="Doe", email="janedoe@email.edu", password="jane", university="UMBC", grad_year="yea", major="major", classes=["no courses", "except this one","bbb"], bio="bio"))
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
        response = self.app.post('/deku/api/users/edit/'+str(id), data=dict(user="carrie@email.edu", pwd="carrie",firstName="Jane", lastName="Doe", email="janedoee@email.edu", password="jane", university="UMBC", grad_year="yea", major="major", classes=["no courses", "except this one","bbb"], bio="bio"))
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
    
    def test_validate_user_method_for_isADMIN(self):
        #edit another user as admin should change name
        id = models.User.query.filter(models.User.email=="carrie@email.edu").first().id
        response = self.app.post('/deku/api/users/edit/'+str(id), data=dict(user="admin@deku.com", pwd="admin",firstName="Jane", lastName="Doe", email="janedoee@email.edu", password="jane", university="UMBC", grad_year="yea", major="major", classes=["no courses", "except this one","bbb"], bio="bio"))
        user = models.User.query.filter(models.User.id==id).first()
        self.assertEquals("Jane",user.firstName)
        
    def test_validate_user_method_for_notADMIN(self):
        #edit another user as non-admin should not change name
        id = models.User.query.filter(models.User.email=="carrie@email.edu").first().id
        response = self.app.put('/deku/api/users/'+str(id), data=dict(user="jane@emailedu", pwd="jane",firstName="Jane", lastName="Doe", email="janedoee@email.edu", password="jane", university="UMBC", grad_year="yea", major="major", classes=["no courses", "except this one","bbb"], bio="bio"))
        user = models.User.query.filter(models.User.id==id).first()
        self.assertNotEquals("Jane",user.firstName)
        
    def test_post_card(self):
        response = self.app.post('/deku/api/cards', data=dict(
                                                        user="janedoe@email.edu",
                                                        pwd="jane",
                                                        content="lesrigfjlaerjf",
                                                        category="cat",
                                                        tags=["one","two"],
                                                        time="time",
                                                        date="date",
                                                        comments=['comment 1','comment 2','comment 3']))
        card = models.Card.query.filter(models.Card.content=="lesrigfjlaerjf").first()
        self.assertEquals(card.user_id, db.session.query(models.User.id).filter(models.User.id==card.user_id).first().id)
        self.assertEquals(card.content,"lesrigfjlaerjf")
        self.assertEquals(card.category,"cat")
        self.assertEquals(card.time,"time")
        self.assertEquals(card.date,"date")
        self.assertEquals(card.tags[0].tag,"one")
        self.assertEquals(card.tags[1].tag,"two")
        self.assertEquals(card.tags2,"one,two")
        self.assertEquals(card.comments[0].comment,"comment 1")
        self.assertEquals(card.comments[1].comment,"comment 2")
        self.assertEquals(card.comments[2].comment,"comment 3")
        
    def test_put_card(self):
        response = self.app.put('/deku/api/cards/1', data=dict(
                                                        user="janedoe@email.edu",
                                                        pwd="jane",
                                                        content="asdf",
                                                        category="sdfg",
                                                        tags=["dfgh","fghj"],
                                                        time="ime",
                                                        date="ate",
                                                        comments=['ghjk 1','hjkl 2','jkl; 3']))
        card = models.Card.query.filter(models.Card.id==1).first()
        self.assertEquals(card.user_id, db.session.query(models.User.id).filter(models.User.id==card.user_id).first().id)
        self.assertEquals(card.content,"asdf")
        self.assertEquals(card.category,"sdfg")
        self.assertEquals(card.time,"ime")
        self.assertEquals(card.date,"ate")
        self.assertEquals(card.tags[0].tag,"dfgh")
        self.assertEquals(card.tags[1].tag,"fghj")
        self.assertEquals(card.tags2,"dfgh,fghj")
        self.assertEquals(card.comments[0].comment,"ghjk 1")
        self.assertEquals(card.comments[1].comment,"hjkl 2")
        self.assertEquals(card.comments[2].comment,"jkl; 3")
        
    def test_delete_card(self):
        response = self.app.post('/deku/api/cards/delete/1', data=dict(user="janedoe@email.edu",pwd="jane"))
        self.assertEquals(models.Card.query.get(1),None)
        
    def test_get_cards(self):
        cards = Card.query.order_by(models.Card.id.desc()).limit(20).all()
        response = self.app.get('/deku/api/cards')
        print response.data
        cards=[card.serialize for card in cards]
        self.assertEquals(json.loads(response.data)['cards'],cards)
        
    def test_get_card(self):
        card = models.Card.query.get(1)
        response = self.app.get('/deku/api/cards/1')
        self.assertEquals(json.loads(response.data)['card'],card.serialize)

    def test_search_by_tag_last20(self):
        response = self.app.get('/deku/api/cards/search/tag/one')
        data = json.loads(response.data)
        self.assertEquals(len(data['cards']),2)
        response = self.app.get('/deku/api/cards/search/tag/two')
        data = json.loads(response.data)
        self.assertEquals(len(data['cards']),1)
        
    def test_search_by_user_last20(self):
        id = models.User.query.filter(models.User.email=="carrie@email.edu").first().id
        response = self.app.get('/deku/api/cards/search/user/'+str(id))
        data = json.loads(response.data)
        self.assertEquals(len(data['cards']),0)
        id = models.User.query.filter(models.User.email=="janedoe@email.edu").first().id
        response = self.app.get('/deku/api/cards/search/user/'+str(id))
        data = json.loads(response.data)
        self.assertEquals(len(data['cards']),2)
        
    def test_mark(self):
        #add jane's first mark to comment 1
        response = self.app.put('/deku/api/cards/1/mark', data=dict(user="janedoe@email.edu",pwd="jane"))
        #add jane's first mark to comment 1 should be an error already exists
        response = self.app.put('/deku/api/cards/1/mark', data=dict(user="janedoe@email.edu",pwd="jane"))
        #add carrie's first mark to comment 1
        response = self.app.put('/deku/api/cards/1/mark', data=dict(user="carrie@email.edu",pwd="carrie"))
        #add jane's first mark to comment 2
        response = self.app.post('/deku/api/cards/2/mark', data=dict(user="janedoe@email.edu",pwd="jane"))
        
    def test_unmark(self):
        response = self.app.put('/deku/api/cards/1/unmark', data=dict(user="janedoe@email.edu",pwd="jane"))

    def test_tags_match(self):
        cards = models.Card.query.all()
        for card in cards:
            newtags = card.tags2.split(",")
            oldtags = [tag.tag for tag in card.tags]
            self.assertEquals(newtags,oldtags)

if __name__ == '__main__':
    unittest.main()
