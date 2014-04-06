#!.venv/bin/python

import os
from flask import Flask, request, jsonify, abort, make_response
from app import app, db, models
from app.utils import cors_response
from flaskext.bcrypt import generate_password_hash, check_password_hash

@app.route('/deku/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return cors_response(jsonify(users = [user.serialize for user in models.User.query.all()]))
    elif request.method == 'POST':
        # TODO check email passed for uniqueness
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        university = request.form.get('university')
        if (firstName and lastName and email and password and university):
            pw_hash = generate_password_hash(password)
            user = models.User(firstName = firstName,
                               lastName = lastName,
                               email = email,
                               password = pw_hash,
                               university = university)
            db.session.add(user)
            db.session.commit()
            return cors_response((jsonify(user = user.serialize), 201))
        else:
            return cors_response(("Bad input", 400))
    else:
        pass

@app.route('/deku/api/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_by_id(user_id):
    if request.method == 'GET':
        user = models.User.query.get(int(user_id))
        if (user):
            return cors_response(jsonify(user = user.serialize))
        else:
            return cors_response(("User not found", 404))
    elif request.method == 'PUT':
        user = models.User.query.get(int(user_id))
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        if (user):
            if (firstName):
                user.firstName = firstName
            if (lastName):
                user.lastName = lastName
            if (email):
                user.email = email
            db.session.commit()
            return cors_response(jsonify(user = user.serialize))
        else:
            return cors_response(("User not found", 404))

    elif request.method == 'DELETE':
        user = models.User.query.get(int(user_id))
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return cors_response(("User deleted.", 200))
        else:
            return cors_response(("No user found.", 204))
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
                correct_pw = check_password_hash(user.password, password)
                if (correct_pw):
                    return cors_response((jsonify(user = user.serialize), 200))

                else:
                    return cors_response(("Wrong password", 401))
            else:
                return cors_response(("User not found", 404))
        else:
            return cors_response(("Email or password missing.", 400))
    else:
        pass
