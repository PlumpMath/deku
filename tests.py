#!.venv/bin/python
import os
import unittest

from config import basedir
from app import app, db
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

    # Test /deku/api/users GET
    def test_get_all_users(self):
        pass

    # Test /deku/api/users POST
    def test_post_new_user(self):
        pass

    # Test /deku/api/users/<int:user_id> GET    
    def test_get_user(self):
        pass

    def test_get_user_fail(self):
        pass

    # Test /deku/api/users/<int:user_id> PUT
    def test_mod_user(self):
        pass

    def test_mod_user_fail(self):
        pass

    # Test /deku/api/users/<int:user_id> DELETE
    def test_delete_user(self):
        pass

    def test_delete_user_fail(self):
        pass

    # Test /deku/api/cards GET
    def test_get_all_cards(self):
        pass

    # Test /deku/api/cards POST
    def test_post_new_card(self):
        pass

    # Test /deku/api/cards/<int:card_id> GET
    def test_get_card(self):
        pass

    def test_get_card_fail(self):
        pass

    # Test /deku/api/cards/<int:card_id> PUT
    def test_mod_card(self):
        pass

    def test_mod_card_fail(self):
        pass

    # Test /deku/api/cards/<int:card_id> DELETE
    def test_delete_card(self):
        pass

    def test_delete_card_fail(self):
        pass

if __name__ == '__main__':
    unittest.main()
