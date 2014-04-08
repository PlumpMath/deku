#!.venv/bin/python

import os
from flask import Flask, request, jsonify, abort, make_response, render_template, json
from sqlalchemy.orm import subqueryload, contains_eager
from app import app, db, models, bcrypt, session
from utils import cors_response


@app.route('/')
def something():
    print 'hello'
    return render_template('index.html')

@app.route('/a', methods=['POST'])
def somethingy():
    print 'something'
    print request.form.get('lastName')
    print request.form['lastName']
    print request.form['hello[]']
    print '---form---'
    print request.form
    print '---data---'
    print request.data
    print '---hello---'
    print request.form.getlist('hello[]')
    return make_response('whatever',200)    
    
@app.route('/asdf')
def somethign():
    password1 = bcrypt.generate_password_hash('password')
    password2 = bcrypt.generate_password_hash('password1')
    user = models.User(firstName="John", lastName="Doe", email="johndoe@email.com",
        password=password1, university="UMBC")
    user2 = models.User(firstName="Jane", lastName="Doe",
        email="janedoe@email.com", password=password2, university="UMBC")
    db.session.add(user)
    db.session.add(user2)
    db.session.commit()

    # Mock cards
    card = models.Card(content="This is a card, and it's pretty basic.", user_id=1)
    card2 = models.Card(content="This is also a card, though it is a bit longer. \
        Just a bit.", user_id=2)
    db.session.add(card)
    db.session.add(card2)
    db.session.commit()
    return cors_response(('whwatever',200))


@app.route('/deku/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return jsonify(users = [user.serialize for user in models.User.query.all()])
    elif request.method == 'POST':
        # TODO check email passed for uniqueness
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')            
        university = request.form.get('university')
        if (firstName and lastName and email and password and university):
            pw_hash = bcrypt.generate_password_hash(password)
            user = models.User(firstName = firstName,
                               lastName = lastName,
                               email = email,
                               password = pw_hash,
                               university = university)
            profile = models.Profile()
            grad_year = request.form.get('grad_year')
            major = request.form.get('major')
            classes = request.form.getlist('classes')
            bio = request.form.get('bio')
            if (grad_year):
                profile.grad_year = grad_year
            if (major):
                profile.major = major
            if isinstance(classes,list):
                for course in classes:
                    temp = models.Course(course=course)
                    profile.courses.append(temp)
                    user.courses.append(temp)
            if (bio):
                profile.bio = bio
            user.profile = profile
            db.session.add(user)
            db.session.commit()
            return make_response(jsonify(user = user.serialize, profile = user.profile.serialize), 201)
        else:
            abort(400)
    else:
        pass

@app.route('/deku/api/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_by_id(user_id):
    if request.method == 'GET':
        user = models.User.query.get(int(user_id))
        if (user):
            return jsonify(user = user.serialize)
        else:
            abort(404)
    elif request.method == 'PUT':
        if u'id' not in session:
            return make_response("not logged in",401)
        if session[u'id'] != user_id:
            return make_response("You cannot modify someone else's information",401)
        
        result = db.session.query(models.User, models.Profile).filter(models.User.id== user_id).filter(models.User.id==models.Profile.user_id).first()
        user =  result.User
        profile = result.Profile
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        university = request.form.get('univ')
        grad_year = request.form.get('grad_year')
        major = request.form.get('major')
        classes = request.form.getlist('classes')
        biography = request.form.get('biography')
        if (user):
            if (firstName):
                user.firstName = firstName
            if (lastName):
                user.lastName = lastName
            if (email):
                user.email = email
            if (password):
                user.password = bcrypt.generate_password_hash(password)
            if (university):
                user.university = university
            if (grad_year):
                profile.grad_year = grad_year
            if (major):
                profile.major = major
            if isinstance(classes,list):
                result = db.session.query(models.Course).filter(models.Course.user_id == session['id']).all()
                for course in result:
                    db.session.delete(course)
                user.courses = []
                profile.courses = []
                for the_class in classes:
                    temp = models.Course(course=the_class)
                    user.courses.append(temp)
                    profile.courses.append(temp)
            if (biography):
                profile.biography = biography
            db.session.commit()
            return make_response(jsonify(user = user.serialize, profile = profile.serialize),200)
        else:
            abort(404)
            
            
    elif request.method == 'DELETE':
        if u'id' not in session:
            return make_response("not logged in", 401)
        user = models.User.query.get(int(user_id))
        if user is not None:
            if session[u'id'] != user.id:
                return make_response("You cannot delete someone elses account",401)
            db.session.delete(user)
            db.session.commit()
            return make_response(("User deleted.", 200))
        else:
            return make_response(("No user found.", 204))
    else:
        pass

@app.route('/deku/api/users/login', methods=['POST'])
def user_authentication():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if (email and password):
            user = models.User.query.filter_by(email=email).first()
            if (user):
                correct_pw = bcrypt.check_password_hash(user.password, password)
                if (correct_pw):
                    session[u'id'] = user.id
                    return make_response(jsonify(user = user.serialize),200)
                else:
                    session.clear()
                    return make_response("invalid",401)
            else:
                session.clear()
                return make_response("user not found",404)
        else:
            session.clear()
            return make_response(("Email or password missing.", 401))
    else:
        session.clear()
        pass

@app.route('/deku/api/users/logged_in')
def check_logged_in():
    if u'id' in session:
        return make_response('logged in',200)
    else:
        return make_response('not logged in',401)
