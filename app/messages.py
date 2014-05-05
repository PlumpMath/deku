#!.venv/bin/python

import os
from flask import Flask, request, jsonify, make_response, json
from app import app, db, models
from app.models import Card
from utils import cors_response
from datetime import datetime

@app.route('/deku/api/messages/<user_id>', methods=['GET', 'POST'])
def messages(user_id):
    if request.method == 'GET':
        user = models.User.query.get(int(user_id))
        if user:
            # Get messages
            messages = models.Message.query.filter(models.Message.to_id == user_id).all()
            return cors_response((jsonify(messages=[message.serialize for message in messages]), 200))
        else:
            return cors_response(("User not found.", 400))

    elif request.method == 'POST':         
        poster_id = request.form.get('poster_id')
        message = request.form.get('message')
        message = models.Message(to_id=user_id,
                                 from_id=poster_id,
                                 message=message,
                                 timestamp=datetime.utcnow())

        db.session.add(message)
        db.session.commit()
        return cors_response((jsonify(message = message.serialize), 201))
    else:
        pass
