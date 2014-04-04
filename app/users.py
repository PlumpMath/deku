#!.venv/bin/python

import os
from flask import Flask, request, jsonify, abort, make_response
from sqlalchemy.orm import subqueryload, contains_eager
from app import app, db, models, bcrypt, session
from cors import crossdomain

@app.route('/deku/api/users', methods=['GET', 'POST'])
@crossdomain(origin='*', methods=['GET', 'POST'])
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
            print password
            print firstName
            print password
            pw_hash = bcrypt.generate_password_hash(password)
            user = models.User(firstName = firstName,
                               lastName = lastName,
                               email = email,
                               password = pw_hash,
                               university = university)
            profile = models.Profile()
            year = request.form.get('year')
            major = request.form.get('major')
            classes = request.form.get('classes')
            biography = request.form.get('biography')
            if (year):
                profile.year = year
            if (major):
                profile.major = major
            if (classes):
                profile.classes = classes
            if (biography):
                profile.biography = biography
            user.profile = profile
            db.session.add(user)
            db.session.commit()
            return make_response(jsonify(user = user.serialize, profile = user.profile.serialize), 201)
        else:
            abort(400)
    else:
        pass

@app.route('/deku/api/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
@crossdomain(origin='*')
def user_by_id(user_id):
    if request.method == 'GET':
        user = models.User.query.get(int(user_id))
        if (user):
            return jsonify(user = user.serialize)
        else:
            abort(404)
    elif request.method == 'PUT':
        print '********----modinfo----'
        if u'id' not in session:
            return make_response("not logged in",401)
        if session[u'id'] != user_id:
            return make_response("You cannot modify someone else's information",401)
        
        result = db.session.query(models.User, models.Profile).filter(models.User.id== user_id).filter(models.User.id==models.Profile.user_id).first()
        user =  result.User
        profile = result.Profile
        #q = models.User.query.filter(models.User.id == user_id).join(models.User.profile)
        print 'aaaa-----------'
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        university = request.form.get('univ')
        year = request.form.get('year')
        major = request.form.get('major')
        classes = request.form.get('classes')
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
            if (year):
                profile.year = year
            if (major):
                profile.major = major
            if (classes):
                profile.classes = classes
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
@crossdomain(origin='*', methods=['POST'])
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
