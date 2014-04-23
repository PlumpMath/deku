from flask import make_response
from sqlalchemy import func
from app import models, bcrypt

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

def authenticateID(user_id, pwd):
    if (user_id and pwd):
        user = models.User.query.get(int(user_id))
        if (user):
            corrent_pw = bcrypt.check_password_hash(user.password, pwd)
            if correct_pw:
                return user
    return None
