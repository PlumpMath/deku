import os
import app
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()

    def tearDown(self):
        pass

    def test_login(self):
        client = app.app.test_client()
        print client.post('/login', data=dict(username='team', password='six')).data
        assert 'Username: team  id: 1' == client.get('/test/login/status').data
        print client.post('/login', data=dict(username='teaM', password='six')).data
        assert 'Username: team  id: 1'== client.get('/test/login/status').data
        print client.post('/login', data=dict(username='team', password='SiX')).data
        assert 'None' == client.get('/test/login/status').data
        print client.post('/login', data=dict(username='TEAM', password='six')).data
        assert 'Username: team  id: 1' == client.get('/test/login/status').data
        print client.post('/login', data=dict(username='teaaaaaam', password='six')).data
        assert 'None' == client.get('/test/login/status').data

    def test_register(self):
        import db.user
        db.user.DropCreateTable()

        client = app.app.test_client()
        print "\n\n\n\n\n\n\n"
        assert 'stored'==client.post('/register', data=dict(username='q',password='b',email='q')).data
        assert ''==client.post('/register', data=dict(username='q',password='b',email='q')).data

if __name__ == '__main__':
    unittest.main()
