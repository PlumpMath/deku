import os
import app
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_stuff(self):
        client = app.app.test_client()
        email = 'a@b.cd'
        password = 'password'
        fields=dict(name="REGIS2", email=email, password=password, university='umbc1',classes="are",major="pain",innn="the",biography="face",graduation_year="1973")
        #register a new user
        print client.post('/register', data=fields).data
        #login with newly registered user
        print client.post('/login',data=dict(email=email, password=password))
        #check status of login
        print client.get('/test/login/status',data=dict(email=email, password=password)).data
        #modify profile information
        print client.post('/editprofile', data=dict(classes="allyour",major="bases",innn="are",biography="arebelong",graduation_year="toUs")).data
        #add a card with 3 tags
        print client.post('/addcard', data=dict(category='cat', content='content', tags=['tagone','tagtwo','tagthree3']))
        

if __name__ == '__main__':
    unittest.main()
