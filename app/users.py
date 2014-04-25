#!.venv/bin/python

from app import app
from app import bcrypt
from app import db
from app import models
from flask import json
from flask import jsonify
from flask import request
from sqlalchemy import func
from utils import cors_response, validate_user

@app.route('/deku/api/users',methods=['GET'])
def get_newest_user():
    return cors_response((jsonify(users = [user.serialize for user in models.User.query.order_by(models.User.id.desc()).limit(20).all()]),200))

@app.route('/deku/api/users/<int:user_id>',methods=['GET'])
def get_user(user_id):
    user = models.User.query.get(int(user_id))
    if (user):
        return cors_response((jsonify(user = user.serialize),200))
    else:
        return cors_response(("User Not Found",400))
    
@app.route('/deku/api/users',methods=['POST'])
def post_new_users():
    data = request.form
    email = data.get('email')
    user = models.User.query.filter(models.User.email==email).first()
    if user:
        return cors_response(("Email already registered",400))
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    password = data.get('password')
    university = data.get('university')
    grad_year = data.get('grad_year')
    major = data.get('major')
    classes = data.getlist('classes[]')
    bio = data.get('bio')
    if firstName and lastName and password and university and email:
        user = models.User(firstName = firstName,
                           lastName = lastName,
                           email = email,
                           password = bcrypt.generate_password_hash(password),
                           university = university)
        profile = models.Profile()
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
        return cors_response(("Missing required fields",400))
        
@app.route('/deku/api/users/delete/<int:user_id>',methods=['POST'])
def delete_user(user_id):
    data = request.form
    user = models.User.query.filter(models.User.id==user_id).first()

    if user is not None:
        if validate_user(user_id):
            models.User.query.filter(models.User.id==user_id).delete()
            db.session.commit()
            return cors_response(("User deleted",200))
        else:
            return cors_response(("Unauthorized Access",401))
    else:
        return cors_response(("User Not Found,204"))

@app.route('/deku/api/users/edit/<int:user_id>',methods=['POST'])
@app.route('/deku/api/users/<int:user_id>',methods=['PUT'])
def modify_user(user_id):
    data = request.form
    user = models.User.query.filter(models.User.id==user_id).first()

    if user is not None:
        if validate_user(user_id):
            #update fields
            firstName = data.get('firstName')
            lastName = data.get('lastName')
            email = data.get('email')
            password = data.get('password')
            university = data.get('university')
            grad_year = data.get('grad_year')
            major = data.get('major')
            classes = data.getlist('classes[]')
            bio = data.get('bio')
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
                courses = models.Course.query.filter(models.Course.user_id==user_id)
                courses.delete()
                for each_class in classes:
                    temp = models.Course(course=each_class)
                    temp.user_id = user.id
                    temp.profile_id = user.profile.id
                    db.session.add(temp)
            if (bio):
                user.profile.bio = bio
            db.session.commit()
            return cors_response((jsonify(user = user.serialize),200))
        else:
            return cors_response(("Unauthorized Access",401))
    else:
        return cors_response(("User not found"))

@app.route('/deku/api/users/login', methods=['POST'])
def user_authentication():
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    if user and pwd:
        user = models.User.query.filter(func.lower(models.User.email)==func.lower(user)).first()
        if (user):
            correct_pw = bcrypt.check_password_hash(user.password, pwd)
            if correct_pw:
                return cors_response((jsonify(user = user.serialize),200))
    return cors_response(("Unauthorized access",401))



