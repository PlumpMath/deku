#!.venv/bin/python

import os
from flask import Flask, request, jsonify, json
from app import app, db, models, bcrypt, generator
from utils import cors_response, authenticate_by_email, authenticate_by_id
from models import ROLE_USER, ROLE_MOD, ROLE_ADMIN

@app.route('/deku/api/users', methods=['GET','POST'])
def users():
    """ GET REQUEST """
    if request.method == 'GET':
        return cors_response((jsonify(users = [user.serialize for user in models.User.query.all()]),200))
    
    """ POST REQUEST """
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
            courses = request.form.get('classes')
            bio = request.form.get('bio')
            avatar = generator.generate(firstName + lastName, 240, 240, output_format="png")

            if (grad_year):
                profile.grad_year = grad_year

            if (major):
                profile.major = major

            if (courses):
                courseList = json.loads(courses)
                user.courses = ",".join(courseList)

            if (bio):
                profile.bio = bio
            
            profile.avatar = avatar

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
            return cors_response(("User not found.", 404))
    else:
        pass

@app.route('/deku/api/users/<int:user_id>', methods=['GET'])
def user_by_id(user_id):
    if request.method == 'GET':
        user = models.User.query.get(int(user_id))
        
        if (user):
            return cors_response((jsonify(user = user.serialize), 200))

        else:
            return cors_response(("User not found.", 404))
    else:
        pass

@app.route('/deku/api/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if request.method == 'POST':
        password = request.form.get('password')
        user = authenticate_by_id(user_id, password)
        if (user is not None):
            if user.role == ROLE_ADMIN:
                return cors_response(("Admin cannot delete own account.", 403))
            else:
                db.session.delete(user)
                db.session.commit()
                return cors_response(("User deleted", 200))
        else:
            return cors_response(("User not found.", 404))
            
    else:
        pass

@app.route('/deku/api/users/update/<int:user_id>', methods=['POST'])
def update_user_by_id(user_id):
    if request.method == 'POST':
        password = request.form.get('confirm_password')
        user = authenticate_by_id(user_id, password)

        if user is None:
            return cors_response(("Unauthorized Access.", 401))
        
        # Update fields
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        university = request.form.get('university')
        grad_year = request.form.get('grad_year')
        major = request.form.get('major')
        courses = request.form.get('classes')
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

        if (courses):
            courseList = json.loads(courses)
            user.courses = ",".join(courseList)

        if (bio):
            user.profile.bio = bio

        db.session.commit()
        return cors_response((jsonify(user = user.serialize), 200))
    else:
        return cors_response(("User not found"))

@app.route('/deku/api/users/login', methods=['POST'])
def user_authentication():
    email = request.form.get('email')
    password = request.form.get('password')
    user = authenticate_by_email(email, password)
    if user:
        return cors_response((jsonify(user = user.serialize),200))
    else:
        return cors_response(("Unauthorized access",401))

@app.route('/deku/api/users/get_avatar/<int:user_id>', methods=['GET'])
def get_user_avatar(user_id):
    user = models.User.query.get(int(user_id))
    if user:
        # Returns a base64 encoded string - can be used as the src in img tag.
        return user.get_avatar
    else:
        pass
