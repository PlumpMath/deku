#!.venv/bin/python

import os, string, random
from flask import Flask, request, jsonify, json
from app import app, db, models, bcrypt, generator
from app.mail import registerEmail, resetPasswordEmail
from utils import cors_response, authenticate_by_email, authenticate_by_id
from models import ROLE_USER, ROLE_MOD, ROLE_ADMIN
from sqlalchemy import or_, func

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
            # Send email to new user.
            registerEmail(email, firstName)
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
        return cors_response(("Unauthorized access", 401))

@app.route('/deku/api/users/get_avatar/<int:user_id>', methods=['GET'])
def get_user_avatar(user_id):
    user = models.User.query.get(int(user_id))
    if user:
        # Returns a base64 encoded string - can be used as the src in img tag.
        return user.get_avatar
    else:
        pass

@app.route('/deku/api/users/follow/<int:user_id>', methods=['POST'])
def follow_user(user_id):
    if request.method == 'POST':
        # Verify user existence.
        user = models.User.query.get(int(user_id))
        if user:
            # Get current user.
            active_user_id = request.form.get("active_id")
            if active_user_id:    
                active_user = models.User.query.get(int(active_user_id))
                if active_user:
                    if user in active_user.following:
                        active_user.following.remove(user)
                    else:
                        active_user.following.append(user)
                    db.session.commit()
                    return cors_response((jsonify(active_user.serialize), 200))
                else:
                    return cors_response(("User not found.", 404))
            else:
                return cors_response(("Bad request.", 400))
        else:
            return cors_response(("User not found.", 404))
    else:
        pass
        
@app.route('/deku/api/users/search/name', methods=['GET'])
def search_by_name():
    names = request.args.get('names')
    output = "wtf"
    names = names.split(",")
    ors = []
    for name in names:
       ors.append(func.lower(models.User.firstName)==func.lower(name))
       ors.append(func.lower(models.User.lastName)==func.lower(name))
    users = models.User.query.filter(or_(*ors)).all()
    return cors_response((jsonify(users = [user.serialize for user in users]),200))

@app.route('/deku/api/users/password', methods=['POST'])
def generateTemporaryPassword():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            # Find user by email address.
            user = models.User.query.filter(models.User.email==email).first()
            if user:
                # Send reset email
                tempPassword = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
                user.password = bcrypt.generate_password_hash(tempPassword)
                db.session.commit()
                resetPasswordEmail(email, user.firstName, tempPassword)
                return cors_response(("Email sent.", 200))                
            else:
                return cors_response(("User not found.", 404))
        else:
            return cors_response(("Bad Request.", 400))
    else:
        pass

@app.route('/deku/api/users/password/<int:user_id>', methods=['POST'])
def resetPassword(user_id):
    if request.method == 'POST':
        user = models.User.query.get(int(user_id))
        if user:
            password = request.form.get("password")
            if password:
                password_hash = bcrypt.generate_password_hash(password)
                user.password = password_hash
                db.session.commit()
                return cors_response((jsonify(user.serialize), 200))
            else:
                return cors_response(("Bad Request.", 400))
        else:
            return cors_response(("User not found.", 404))
    else:
        pass
                  
@app.route('/deku/api/users/notification/delete/<int:user_id>', methods=['POST'])
def deleteNotification(user_id):
    if request.method == 'POST':
        # Verify card existence:
        user = models.User.query.get(int(user_id))
        if (user):
            # set up data fields for notification
            notification_id = request.form.get('notification_id')
            notification = models.Notification.query.get(notification_id)
            if (notification):
                user.notifications.remove(notification)
                db.session.commit()
                return cors_response((jsonify(user.serialize), 200))
            else:
                return cors_response(("Notification doesn't exist", 404))
        else:
            return cors_response(("User doesn't exist.", 404))
    else:
        pass

@app.route('/deku/api/users/hidden/<int:user_id>', methods=['POST'])
def hideUser(user_id):
    if request.method == 'POST':
        user = models.User.query.get(int(user_id))
        if user:
            active_user_id = request.form.get("active_id")
            if active_user_id:
                active_user = models.User.query.get(int(active_user_id))
                if active_user:
                    if user in active_user.usersHidden:
                        active_user.usersHidden.remove(user)
                    else:
                        active_user.usersHidden.append(user)
                    db.session.commit()
                    return cors_response((jsonify(user.serialize), 200))
                else:
                    return cors_response(("User not found.", 404))
            else:
                return cors_response(("Bad Request.", 400))
        else:
            return cors_response(("User not found.", 404))
    else:
        pass
