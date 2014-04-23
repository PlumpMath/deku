from flask import make_response
from app import models, bcrypt

def cors_response(response):
    resp = make_response(response)
    resp.headers['Access-Control-Allow-Origin'] = "http://localhost:4567"
    return resp

def authenticate(user_id, password):
    if (user_id and password):
        user = models.User.query.get(int(user_id))
        if (user):
            correct_pw = bcrypt.check_password_hash(user.password, pwd)
            if correct_pw:
                return user
    return None
