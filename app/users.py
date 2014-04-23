#!.venv/bin/python

import os
from flask import Flask, request, jsonify, abort, render_template, json
from sqlalchemy.orm import subqueryload, contains_eager
from app import app, db, models, bcrypt, session
from utils import cors_response, authenticate_by_email, authenticate_by_id
from models import ROLE_USER, ROLE_MOD, ROLE_ADMIN

@app.route('/deku/api/users', methods=['GET','POST'])
def users():
    if request.method == 'GET':
        return cors_response((jsonify(users = [user.serialize for user in models.User.query.all()]),200))

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
            return cors_response(("Bad Request.", 400))
    else:
        pass

#This is used to set a user to be an administrator. Possibly a temporary solution, I just needed some way to make this happen
@app.route('/deku/api/users/make_admin/<int:user_id>', methods=['PUT'])
def make_user_admin(user_id):
    if request.method == 'PUT':
        user = models.User.query.get(int(user_id))
        if (user):
            user.role = 2
            db.session.commit()
            return cors_response((jsonify(user = user.serialize), 200))
        else:
            return cors_response(("Invalid Request", 400))
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
        password = request.form.get('confirm_password')
        user = authenticate_by_id(user_id, password)

        if not isinstance(user, models.User):
            return cors_response(("Unauthorized Access",401))
        
        if user is None:
            return cors_response(("User Not Found",204))
        
        # Update fields
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
            existing_courses = [] 
            
            for course in user.courses:
                if course.course not in classes:
                    db.session.delete(course)
                else:
                    existing_courses.append(course.course)

            for course in classes:
                if course not in existing_courses:
                    temp = models.Course(course = course)
                    temp.user_id = user.id
                    temp.profile_id = user.profile.id
                    db.session.add(temp)
        
        if (bio):
            user.profile.bio = bio

        db.session.commit()
        return cors_response((jsonify(user = user.serialize), 200))

    elif request.method == 'DELETE':
        password = request.get("password")
        user = authenticate_by_id(user_id, password)
        if (user):
            if user.role == ROLE_ADMIN:
                return cors_response(("Admin cannot delete own account.", 403))
            else:
                db.session.delete(user)
                return cors_response(("User deleted", 200))
        else:
            return cors_response(("User not found.", 404))
            
    else:
        pass

@app.route('/deku/api/users/login', methods=['POST', 'GET'])
def user_authentication():
    email = request.form.get('email')
    password = request.form.get('password')
    user = authenticate_by_email(email, password)
    if user:
        return cors_response((jsonify(user = user.serialize),200))
    else:
        return cors_response(("Unauthorized access",401))
