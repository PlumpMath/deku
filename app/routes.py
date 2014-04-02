#!.venv/bin/python
import random,string
from flask import Flask, request, jsonify, abort, make_response, session
from app import app, db, models, bcrypt,logged_in
import time


@app.route('/something', methods=['GET', 'POST'])
def something():
    #all this stuff works
    #register user
    #update profile
    #login
    print time.time() - time.time()
    something=''
    firstName='first'
    lastName='lastname'
    email='email'
    univ='un'
    user = models.User(firstName = firstName, lastName = lastName,email = email, univ=univ)
    db.session.add(user)
    db.session.commit()
    print user
    print 'wtf'
    
    firstName='secondname'
    lastName='lastagain'
    email='email@a.a'
    user = models.User(firstName = firstName, lastName = lastName,email = email)
    db.session.add(user)
    db.session.commit()
    profile=models.Profile(year="ye", major="ma", bio="bi", classes="whatever")
    user.profile= profile
    db.session.commit()
    
    
    users = models.User.query.all()
    for user in users:
        something += str(user)
        print user
    print user
    user.profile.major = "something else"
    user = models.User.query.get(2)
    print user.profile
    db.session.commit()
    card = models.Card(content="something", category="cat")
    card2 = models.Card(content="something2", category="cat2")
    user.cards.append(card)
    user.cards.append(card2)
    cards = user.cards
    tag1= models.Tag("one")
    tag2= models.Tag("two")
    tag3=models.Tag("one")
    card.tags.append(tag1)
    card.tags.append(tag2)
    card2.tags.append(tag3)
    db.session.commit()
    print cards
    for card in cards:
        print card
    cards = [card.serialize for card in models.Card.query.all()]
    print cards

    return make_response(something)

@app.route('/somethingy', methods=['GET','POST'])
def somethingy():
    user = models.User.query.get(2)
    print user
    cards = [card.serialize for card in models.Card.query.all()]
    mystr=""
    for card in cards:
        mystr = mystr+ str(card)
    result = card_by_tag('one')
    print result.data
    return make_response(mystr)


#this works
#to create a new user, call using POST
#provides a token if client decides that the 'register' will also login the user.
#token can be used to modify fields /deku/api/users/<int:user_id> PUT
@app.route('/deku/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return jsonify(users = [user.serialize for user in models.User.query.all()])
    elif request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        univ = request.form.get('univ')
        if email:
            user = models.User.query.filter(models.User.email == email).first()
            if user:
                return make_response(jsonify({'error':'Email exists in database.'}), 409)#409 conflict
            
        if (firstName and lastName and univ and password):
            pw_hash = bcrypt.generate_password_hash(password)
            user = models.User(firstName = firstName,
                               lastName = lastName,
                               email = email,
                               univ = univ,
                               password = pw_hash)
            db.session.add(user)
            db.session.commit()
            token = ''.join(random.choice(string.printable) for _ in range(77))
            logged_in[unicode(user.id)] = token
                
            return make_response(jsonify(user = user.serialize, token=token),201)
        else:
            return abort(400)
    else:
        pass


#/deku/api/users/<int:user_id> PUT is working
#same as before except now requires email:password or a token(from logging in. see /deku/api/users/login) 
#get looks fine
#didn't add auth to delete yet
@app.route('/deku/api/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_by_id(user_id):
    if request.method == 'GET':
        user = models.User.query.get(int(user_id))
        if (user):
            return make_response(jsonify(user = user.serialize),200)
        else:
            abort(404)
    elif request.method == 'PUT':
        form = dict()
        form['email']=request.form.get('email')
        form['token']=request.form.get('token')
        form['password']=request.form.get('password')
        form['id'] = user_id
        auth = auth_helper(form)
        user = models.User.query.get(int(user_id))
        if user:
            pass
        else:
            return make_response(jsonify({"error":"User doesn't exist"}),404)
        if auth:
            user = models.User.query.get(int(user_id))
            if user:
                if user.id != user_id:
                    return make_response(jsonify({"You can not modify someone elses info"}),401)
            firstName = request.form.get('firstName')
            lastName = request.form.get('lastName')
            email = request.form.get('email')
            univ = request.form.get('univ')#not tested
            bio = request.form.get('bio')#not tested
            classes= request.form.get('classes')#not tested
            year = request.form.get('year')#not tested
            major = request.form.get('major')#not tested
        
            if (user):
                if (firstName):
                    user.firstName = firstName
                if (lastName):
                    user.lastName = lastName
                if (email):
                    user.email = email
                #todo univ, bio, classes, year, major
                db.session.commit()
                return jsonify(user = user.serialize)
            else:
                abort(404)
        else:
            return make_response("Invalid token or email:password",401)

    elif request.method == 'DELETE':
        user = models.User.query.get(int(user_id))
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return make_response(("User deleted.", 200, None))
        else:
            return make_response(("No user found.", 204, None))
    else:
        pass

#if successful, returns a token to be used for authentication.
@app.route('/deku/api/users/login', methods=['POST'])
def user_authentication():
    if request.method == 'POST':
        form = request.form
        return auth_helper(form)
    else:
        pass

#place this at beginning of each thing that requries authentication 
def auth_helper(form):
    email = form.get('email')
    password = form.get('password')
    token = form.get('token')
    id = form.get('id')
    #check encrypted cookie session first
    #if 'logged_in' in session:
    #    user = models.User.query.get(session['id'])
    #    if user:
    #        return jsonify(user = user.serialize, token = token)
    #    else:
    #        return make_response("Horrible unknown error", 400)
        
    #if not using encrypted cookie session, try id and token
    if (id and token):
        if logged_in[unicode(id)] == token:
            user = models.User.query.get(id)
            if user:
                return jsonify(user = user.serialize, token = token)
            else:
                return make_response("Horrible unknown error, Probably account deleted after login somehow", 400)
        else:
            return make_response("Invalid token. Perhaps logged in from elsewhere", 401)

    #if no persistent state, or not logged in, go email:password        
    if (email and password):
        user = models.User.query.filter_by(email = email).first()
        if(user):
            correct_pw = bcrypt.check_password_hash(user.password, password)
            if (correct_pw):
                #for session users
                #session['logged_in'] = True
                #session['id'] = user.id
                #make token
                token = ''.join(random.choice(string.printable) for _ in range(77))
                #session['token'] = token
                
                #for token users
                logged_in[unicode(user.id)] = token
                
                return jsonify(user = user.serialize, token=token)
            else:
                return make_response("Invalid Password",401)
        else:
            return make_response("Unregistered Email", 401)

    #fail    
    session.clear()
    return None
                
                
            
@app.route('/deku/api/cards', methods=['GET', 'POST'])
def cards():
    if request.method == 'GET':
        return jsonify(cards = [card.serialize for card in models.Card.query.all()])
    elif request.method == 'POST':
        content = request.form.get('content')
        if (content):
            card = models.Card(content = content)
            db.session.add(card)
            db.session.commit()
            print card
            return make_response(('Card created.', 201, None))
        else:
            return abort(400)
    else:
        pass

@app.route('/deku/api/cards/<int:card_id>', methods=['GET', 'PUT', 'DELETE'])
def card_by_id(card_id):
    if request.method == 'GET':
        card = models.Card.query.get(int(card_id))
        if (card):
            return jsonify(card = card.serialize)
        else:
            return abort(404)
    elif request.method == 'PUT':
        card = models.Card.query.get(int(card_id))
        content = request.form.get('content')
        if (card):
            if (content):
                card.content = content
            db.session.commit()
            return make_response(("Card modified.", 200, None))
        else:
            return abort(404)

    elif request.method == 'DELETE':
        card = models.Card.query.get(int(card_id))
        if (card):
            db.session.delete(card)
            db.session.commit()
            return make_response(("Card deleted.", 200, None))
        elif (card is None):
            return make_response(("No card found.", 204, None))
    else:
        pass


@app.route('/deku/api/cards/userID/<int:user_id>', methods=['GET', 'PUT'])
def card_by_user_id(user_id):
    if request.method=='GET':
        result = models.Card.query.filter(models.Card.user_id == user_id).all()
        return jsonify(cards = [card.serialize for card in result])
    elif request.method=='PUT':
        pass
    
@app.route('/deku/api/cards/tag/<tag>', methods=['GET', 'PUT'])
def card_by_tag(tag):
    if request.method=='GET':
        result = models.Card.query.filter(models.Tag.tag == tag).all()
        return jsonify(cards = [card.serialize for card in result])
    elif request.method=='PUT':
        pass

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0:3333')

