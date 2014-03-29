import os
import app
import unittest
import tempfile
from flask import json
from db.config import DropCreateTable

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        DropCreateTable()

    def tearDown(self):
        pass
    
    def test_stuff(self):
        client = app.app.test_client()
        email = 'aw@efkif.cj'
        password = 'password'
        fields=dict(firstname="first",lastname="last", email=email, password=password, university='umbc1',classes="are",major="pain",innn="the",bio="face",year="1973")
        
        #register a new user
        print "--------------------REGISTER"
        result = client.post('/register', data=fields).data
        result = json.loads(result)
        if 'errors' in result:
            print "--------------------ERRORSINREGITSTER"
            print result['errors']
        else:
            #edit profile
            print "---------------EDITPROFILE1"
            print client.post('/editprofile',data=fields).data
        
        #login
        print "---------------LOGIN"
        print client.post('/login',data=dict(email=email, password=password)).data
        
        #edit profile again
        print "---------------EDITPROFILE2"
        print client.post('/editprofile', data=dict(classes="allyour",major="bases",innn="are",bio="arebelong",year="toUs"))
        
        #add a card with 3 tags
        tags=json.dumps(['one','two','three'])
        print client.post('/addcard', data=dict(category='ctgry', content='cntnt', tags=tags))
        #get last 2 cards posted in json form
        #currently returns a "python list" of cards...   [ {id:}{user_id:}{tags:[1,2,...]}{created:}{content} , card2 , card3 ]
        #print vars(client.get('/getCards?numCards=2'))
        

if __name__ == '__main__':
    unittest.main()
