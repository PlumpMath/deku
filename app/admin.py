#!.venv/bin/python

import os
from flask import Flask, request, jsonify, json
from app import app, db, models, bcrypt
from utils import cors_response, authenticate_by_email, authenticate_by_id
from models import ROLE_MOD

@app.route('deku/api/admin/users/make_moderator/<int:user_id>', methods=['POST'])
def makeModerator(user_id):
    if request.method == 'POST':
        user = models.User.query.get(int(user_id))
        if (user): 
            admin_id = request.form.get("admin_id")
            admin_password = request.form.get("admin_password")
            if (admin_id and admin_password):
                admin = authenticate_by_id(admin_id, admin_password)
                if (admin):
                    user.role = ROLE_MOD
                    db.session.commit()
                    return cors_response(("User is now an admin.", 200))
                else:
                    return cors_response(("Unauthorized.", 403))
            else:
                return cors_response(("Bad Request.", 400))
        else:
            return cors_response(("User not found.", 404))
    else:
        pass 
                    

@app.route('deku/api/admin/users/delete/<int:user_id>', methods=['DELETE'])
def deleteUser(user_id):
    if request.method == 'DELETE':
        user = models.User.query.get(int(user_id))
        if (user):
            admin_id = request.form.get("admin_id")
            admin_password = request.form.get("admin_password")
            if (admin_id and admin_password):
                admin = authenticate_by_id(admin_id, admin_password)
                if (admin):
                    db.session.delete(user)
                    db.session.commit()
                    return cors_response(("User deleted.", 200))
                else:
                    return cors_response(("Unauthorized.", 403))
            else:
                return cors_response(("Bad Request.", 400))
        else:
            return cors_response(("User not found.", 404))
    else:
        pass
