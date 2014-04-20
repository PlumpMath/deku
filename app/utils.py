from flask import make_response
from sqlalchemy import func
from app import bcrypt, app, session
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

def authenticate(email, pwd):
    if (email and pwd):
        user = models.User.query.filter(func.lower(models.User.email)==func.lower(email)).first()
        if (user):
            correct_pw = bcrypt.check_password_hash(user.password, pwd)
            if correct_pw:
                return user
    return None