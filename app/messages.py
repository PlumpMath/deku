#!.venv/bin/python

import os
from flask import Flask, request, jsonify, abort, make_response, json
from app import app, db, models, session
from app.models import Card
from utils import cors_response, authenticate_by_email, authenticate_by_id
import time

#UNAUTHENTICATED AND USERS' EXISTENCE UNCHECKED
@app.route('/deku/api/messages/<id>', methods=['GET', 'POST'])
def messages(id):
    if request.method == 'GET':
        if id:
            return cors_response((jsonify(messages=[message.serialize for message in models.Message.query.filter(models.Message.to_id==id).all()]),200))
        return cors_response(("error",400))

    elif request.method == 'POST':         
        poster_id = request.form.get('poster_id')
        message = request.form.get('message')
        message = models.Message(to_id=id, from_id=poster_id, message=message,timestamp=time.ctime())

        db.session.add(message)
        db.session.commit()
        return cors_response((jsonify(message = message.serialize), 201))
    else:
        pass
