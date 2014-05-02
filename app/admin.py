#!.venv/bin/python

import os
from flask import Flask, request, jsonify, json
from app import app, db, models, bcrypt
from utils import cors_response, authenticate_by_email, authenticate_by_id
from models import ROLE_MOD, ROLE_USER

@app.route('/deku/api/admin/users/make_moderator/<int:user_id>', methods=['POST'])
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
                    return cors_response(("User is now a moderator.", 200))
                else:
                    return cors_response(("Unauthorized.", 403))
            else:
                return cors_response(("Bad Request.", 400))
        else:
            return cors_response(("User not found.", 404))
    else:
        pass 


@app.route('/deku/api/admin/users/make_user/<int:user_id>', methods=['POST'])
def makeUser(user_id):
    if request.method == 'POST':
        user = models.User.query.get(int(user_id))
        if (user): 
            admin_id = request.form.get("admin_id")
            admin_password = request.form.get("admin_password")
            if (admin_id and admin_password):
                admin = authenticate_by_id(admin_id, admin_password)
                if (admin):
                    user.role = ROLE_USER
                    db.session.commit()
                    return cors_response(("User is no longer a moderator.", 200))
                else:
                    return cors_response(("Unauthorized.", 403))
            else:
                return cors_response(("Bad Request.", 400))
        else:
            return cors_response(("User not found.", 404))
    else:
        pass 


@app.route('/deku/api/admin/users/delete/<int:user_id>', methods=['POST'])
def deleteUser(user_id):
    if request.method == 'POST':
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


@app.route('/deku/api/admin/cards/delete/<int:card_id>', methods=['POST'])
def deleteCard(card_id):
    if request.method == 'POST':
        card = models.Card.query.get(int(card_id))
        if (card):
            admin_id = request.form.get("admin_id")
            admin_password = request.form.get("admin_password")
            if (admin_id and admin_password):
                admin = authenticate_by_id(admin_id, admin_password)
                if (admin):
                    db.session.delete(card)
                    db.session.commit()
                    return cors_response(("Card deleted.", 200))
                else:
                    return cors_response(("Unauthorized.", 403))
            else:
                return cors_response(("Bad Request.", 400))
        else:
            return cors_response(("Card not found.", 404))
    else:
        pass
