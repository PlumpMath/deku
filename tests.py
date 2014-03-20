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
        client.post('/login', data=dict(email='test@test.test', password='password')).data
        print client.get('/test/login/status').data
        client.post('/login', data=dict(email='TEST@TEST.TEST', password='password')).data
        print client.get('/test/login/status').data
        client.post('/login', data=dict(email='team', password='SiX')).data
        print client.get('/test/login/status').data
        
    def test_register(self):
        client = app.app.test_client()
        print client.post('/register', data=dict(name="REGIS", email='regis@ter.ifng', password='password', university='umbc')).data
        print client.get('/test/login/status').data
        client.post('/editprofile', data=dict(major='regis', do='tur', graduation_year='ing')).data
        client.post('/login', data=dict(email='regis@ter.ifng', password='password')).data
        
        
        #import db.user
        #db.user.DropCreateTable()
        
        #client = app.app.test_client()
        #client.post()
        #print "\n\n\n\n\n\n\n"
        #assert 'stored'==client.post('/register', data=dict(username='q',password='b',email='q')).data
        #assert ''==client.post('/register', data=dict(username='q',password='b',email='q')).data
        
    def test_profile(self):
        client = app.app.test_client()
        client.post('/login', data=dict(username='test@test.test', password='password')).data
        client.post('/editprofile', data=dict(major='mmmajorrr', do='nothing', graduation_year='gggrad')).data

if __name__ == '__main__':
    unittest.main()
