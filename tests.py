#!.venv/bin/python
import os
import unittest
import urllib2

from flask import json
from config import basedir
from app import app, db, bcrypt
from app.models import User, Card

class APITestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

        # Mock users
        password1 = bcrypt.generate_password_hash('password')
        password2 = bcrypt.generate_password_hash('password1')
        user = User(firstName="John", lastName="Doe", email="johndoe@email.com",
                password=password1)
        user2 = User(firstName="Jane", lastName="Doe",
                email="janedoe@email.com", password=password2)
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()

        # Mock cards
        card = Card(content="This is a card, and it's pretty basic.", user_id=1)
        card2 = Card(content="This is also a card, though it is a bit longer. \
                Just a bit.", user_id=2)
        db.session.add(card)
        db.session.add(card2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Test /deku/api/users GET
    def test_get_all_users(self):
        response = self.app.get('/deku/api/users')
        self.assertIsNotNone(response.get_data())

    # Test /deku/api/users POST
    def test_post_new_user(self):
        response = self.app.post('/deku/api/users', data = dict(
            firstName = "Carrie",
            lastName = "Hildebrand",
            email = "carrie.hildebrand@gmail.com",
            password = bcrypt.generate_password_hash('password2')))
        self.assertEquals(response.status_code, 201)

    def test_post_new_user_bad_request(self):
        response = self.app.post('/deku/api/users', data = dict(
            firstName = "Peter"))
        self.assertEquals(response.status_code, 400)

    # Test /deku/api/users/<int:user_id> GET    
    def test_get_user(self):
        response = self.app.get('/deku/api/users/1')
        self.assertIn("John", response.get_data())

    def test_get_user_fail(self):
        response = self.app.get('/deku/api/users/5')
        self.assertEquals(response.status_code, 404)

    # Test /deku/api/users/<int:user_id> PUT
    def test_mod_user(self):
        response = self.app.put('/deku/api/users/1', data=dict( firstName="Lucas"))
        self.assertIn("Lucas", response.get_data())

    def test_mod_user_fail(self):
        response = self.app.put('/deku/api/users/5', data=dict( lastName="Hood"))
        self.assertEquals(response.status_code, 404)

    # Test /deku/api/users/<int:user_id> DELETE
    def test_delete_user(self):
        response = self.app.delete('/deku/api/users/1')
        self.assertEquals(response.status_code, 200)

    def test_delete_user_fail(self):
        response = self.app.delete('/deku/api/users/8')
        self.assertEquals(response.status_code, 204)

    def test_user_login(self):
        response = self.app.post('/deku/api/users/login', data = dict(
            email="johndoe@email.com",
            password="password"))
        self.assertEquals(response.status_code, 200)

    def test_user_login_bad_password(self):
        response = self.app.post('/deku/api/users/login', data = dict(
            email="johndoe@email.com",
            password="blahblahblah"))
        self.assertEquals(response.status_code, 401)

    def test_user_login_user_does_not_exist(self):
        response = self.app.post('/deku/api/users/login', data = dict(
            email="boristhesovietlovehammer@motherrussia.ru",
            password="putinismycomrade"))
        self.assertEquals(response.status_code, 404)

    # Test /deku/api/cards GET
    def test_get_all_cards(self):
        response = self.app.get('/deku/api/cards')
        self.assertIsNotNone(response.get_data())

    # Test /deku/api/cards POST
    def test_post_new_card(self):
        response = self.app.post('/deku/api/cards', data = dict(
            content = "This is the text for a new card! It's a pretty awesome one."
        ))
        self.assertEquals(response.status_code, 201)

    def test_post_new_card_fail(self):
        response = self.app.post('/deku/api/cards', data = dict())
        self.assertEquals(response.status_code, 400)

    # Test /deku/api/cards/<int:card_id> GET
    def test_get_card(self):
        response = self.app.get('/deku/api/cards/1')
        self.assertIn("This is a card, and it's pretty basic.", response.get_data())

    def test_get_card_fail(self):
        response = self.app.get('/deku/api/cards/4')
        self.assertEquals(response.status_code, 404)

    # Test /deku/api/cards/<int:card_id> PUT
    def test_mod_card(self):
        response = self.app.put('/deku/api/cards/1', data=dict( content="Apples"))
        self.assertEquals(response.status_code, 200)

    def test_mod_card_fail(self):
        response = self.app.put('/deku/api/cards/5', data=dict( content="Bananas"))
        self.assertEquals(response.status_code, 404)

    # Test /deku/api/cards/<int:card_id> DELETE
    def test_delete_card(self):
        response = self.app.delete('/deku/api/cards/2')
        self.assertEquals(response.status_code, 200)

    def test_delete_card_fail(self):
        response = self.app.delete('/deku/api/cards/5')
        self.assertEquals(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()
