#!.venv/bin/python

import os
from flask import Flask, request, jsonify, abort, render_template, json
from sqlalchemy.orm import subqueryload, contains_eager
from app import app, db, models, bcrypt, session
from utils import cors_response, authenticate

@app.route('/deku/api/users', methods=['GET','POST'])
def users():
    if request.method == 'GET':
        return jsonify(users = [user.serialize for user in models.User.query.all()])
    if request.method == 'POST':
        email = request.form.get('email')
        user = models.User.query.filter(models.User.email==email).first()
        if user:
            return cors_response(("Email already registered",400))
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
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
            return cors_response((jsonify(user = user.serialize), 201))
        else:
            cors_response(("Invalid Request. First and Last names, email, password, university must all be present",400 ))
    else:
        pass

@app.route('/deku/api/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_by_id(user_id):
    if request.method == 'GET':
        user = models.User.query.get(int(user_id))
        if (user):
            return cors_response((jsonify(user = user.serialize),200))
        else:
            return cors_response(("Invalid Request",400))
    elif request.method == 'PUT':
        #authenticate
        user = request.form.get('user')
        pwd = request.form.get('pwd')
        user = authenticate(user, pwd)
        if not isinstance(user, models.User):
            return cors_response(("Unauthorized Access",401))
        
        #if you're not logged in as the user you're either trying to mod someone elses info or you're an admin
        if user.id!= user_id:
            #you must be an admin or else you're not allowed to delete the stuff
            if user.role != models.ROLE_ADMIN:
                return cors_response(("Unauthorized Access 1",401))
            else:
                #we're an admin editing someone elses stuff so let's get that stuff so we edit that instead of our own info.
                user = models.User.query.get(int(user_id))
                print 'wtf'
                if user is None:
                    print 'wtf2'
                    return cors_response(("User Not Found",204))
        
        #update fields
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        university = request.form.get('university')
        grad_year = request.form.get('grad_year')
        major = request.form.get('major')
        classes = request.form.getlist('classes')
        bio = request.form.get('bio')
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
            user.profile.grad_year = grad_year
        if (major):
            user.profile.major = major
        if isinstance(classes,list):
            result = db.session.query(models.Course).filter(models.Course.user_id == user.profile.user_id).all()
            already_there = [] 
            for course in user.courses:
                if course.course not in classes:
                    db.session.delete(course)
                else:
                    already_there.append(course.course)
            for each_class in classes:
                if each_class not in already_there:
                    temp = models.Course(course=each_class)
                    temp.user_id = user.id
                    temp.profile_id = user.profile.id
                    db.session.add(temp)
        if (bio):
            user.profile.bio = bio

        db.session.commit()
        return cors_response((jsonify(user = user.serialize),200))

    elif request.method == 'DELETE':
        #authenticate
        user = request.form.get('user')
        pwd = request.form.get('pwd')
        user = authenticate(user, pwd)
        if not isinstance(user, models.User):
            return cors_response(("Unauthorized Access",401))
        
        #must be user or admin to delete
        if user.id!=user_id:
            if user.role != models.ROLE_ADMIN:
                return cors_response(("Unauthorized Access",401))
            else:
                user = models.User.query.filter(models.User.id==user_id)
                if user is None:
                    return cors_response(("User Not Found", 204))
        
        db.session.delete(user)
        return cors_response(("User deleted.", 200))
    else:
        pass

@app.route('/deku/api/users/login', methods=['POST', 'GET'])
def user_authentication():
    user = request.form.get('email')
    pwd = request.form.get('password')
    user = authenticate(user, pwd)
    if user:
        return cors_response((jsonify(user = user.serialize),200))
    else:
        return cors_response(("Unauthorized access",401))