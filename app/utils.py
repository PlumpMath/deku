from flask import make_response
from flask import request
from sqlalchemy import func
from app import bcrypt, app, session,db
from app import models
import time

@app.before_request
def auth_stuff():
    #if logged in, check inactivity
    if "time" in session:
        now = time.time()
        inactive_seconds = now-session['time']
        if inactive_seconds > 1800:
            session.clear()
        else:
            #reset timer
            session['time'] = now
            
def cors_response(response):
    resp = make_response(response)
    resp.headers['Access-Control-Allow-Origin'] = "http://localhost:4567"
    return resp

#if no user_id is sent in, valid user/pwd combination returns: user id of that user/pwd combination
#if user_id is sent in, valid user/pwd and [(user_id matches id of user/pwd combo) or (user is an admin))]: user_id sent in 
def validate_user(user_id=None):
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    #user = db.session.query(models.User.id, models.User.role, models.User.password).filter(func.lower(models.User.email)==func.lower(user)).first()
    user = db.session.query(models.User.firstName,models.User.id, models.User.role, models.User.password).filter(func.lower(models.User.email)==func.lower(user)).first()
    if user:
        if bcrypt.check_password_hash(user.password, pwd):
            if user_id is None:
                return user.id
            if user.id==user_id or user.role==models.ROLE_ADMIN:
                return user_id
    return None