#!.venv/bin/python

import os
from flask import Flask, request, jsonify, abort, render_template, json
from sqlalchemy.orm import subqueryload, contains_eager
from sqlalchemy import func
from app import app, db, bcrypt, session
from app import models
from utils import cors_response, authenticate
import time
from flask.views import MethodView

@app.route('/')
def something():
    print session['user']
    return cors_response((session['user']['firstName']))

class UserAPI(MethodView):
    def get(self, user_id):
        if user_id is None:
            return cors_response((jsonify(users = [user.serialize for user in models.User.query.all()]),200))
        else:
            user = models.User.query.get(int(user_id))
            if (user):
                return cors_response((jsonify(user = user.serialize),200))
            else:
                return cors_response(("Invalid Request",400))

    #modify user info
    #email, password, firstName, lastName, university, grad_year, major, classes[], bio 
    def post(self):
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

    def delete(self, user_id):
        if 'user' not in session:
            return cors_response(("Unauthorized Access",401))
        
        #must be user or admin to delete
        if session['user'].get('id')!=user_id:
            if session['user'].get('role') != models.ROLE_ADMIN:
                return cors_response(("Unauthorized Access 1",401))

        user = models.User.query.filter(models.User.id==user_id).first()
        if user is None:
            return cors_response(("User Not Found", 204))
        
        db.session.delete(user)
        db.session.commit()
        return cors_response(("User deleted.", 200))

    def put(self, user_id):

        if 'user' not in session:
            return cors_response(("Unauthorized Access",401))
        #if you're not logged in as the user you're either trying to mod someone elses info or you're an admin
        if session['user'].get('id')!= user_id:
            #you must be an admin or else you're not allowed to delete the stuff
            if session['user'].get('role') != models.ROLE_ADMIN:
                return cors_response(("Unauthorized Access 1",401))

        user = models.User.query.filter(models.User.id==user_id).first()
        if user is None:
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

user_view = UserAPI.as_view('user_api')
app.add_url_rule('/deku/api/users', defaults={'user_id': None},
                 view_func=user_view, methods=['GET',])
app.add_url_rule('/deku/api/users', view_func=user_view, methods=['POST',])
app.add_url_rule('/deku/api/users/<int:user_id>', view_func=user_view,
                 methods=['GET', 'PUT', 'DELETE'])

@app.route('/deku/api/users/login', methods=['POST'])
def user_authentication():
    user = request.form.get('email')
    pwd = request.form.get('password')
    if user and pwd:
        user = models.User.query.filter(func.lower(models.User.email)==func.lower(user)).first()
        if (user):
            correct_pw = bcrypt.check_password_hash(user.password, pwd)
            if correct_pw:
                session['user']=user.serialize
                return cors_response((jsonify(user = user.serialize),200))
    session.clear()
    return cors_response(("Unauthorized access",401))

@app.route('/deku/api/users/logout',methods=['PUT'])

#same as attempting to login with no credentials
def logout():
    session.clear()
    return cors_response(("logged out",200))

@app.route('/deku/api/users/check_login',methods=['GET'])
def check_login():
    if 'user' in session:
        return cors_response(("good",200))
    else:
        return cors_response(("bad",401))

