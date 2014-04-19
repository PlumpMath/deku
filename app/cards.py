#!.venv/bin/python

import os
from flask import Flask, request, jsonify, abort, make_response, json
from app import app, db, models, session
from app.models import Card
from utils import cors_response, authenticate

@app.route('/deku/api/cards', methods=['GET', 'POST'])
def cards():
    if request.method == 'GET':
        return cors_response((jsonify(cards = [card.serialize for card in Card.query.all()]), 200))
    elif request.method == 'POST':
        #authenticate
        #The user is not going to give their password each time they post a card
        #user = request.form.get('user')
        #pwd = request.form.get('password')
        #user = authenticate(user, pwd)
        #if not isinstance(user, models.User):
        #    return cors_response(("Unauthorized Access. Login to post a card",401))
        
        content = request.form.get('content')
        category = request.form.get('category')
        tags = request.form.getlist('tags')
        author = request.form.get('author')
        author_id = request.form.get('author_id')
        if (content):
            card = models.Card(user_id = author_id,
                               content=content,
                               user= author)
            if (category):
                card.category = category
            for tag in tags:
                card.tags.append(models.Tag(tag))
            db.session.add(card)
            db.session.commit()
            return cors_response((jsonify(card = card.serialize), 201))
        else:
            return cors_response(("Invalid request", 400))
    else:
        pass

@app.route('/deku/api/cards/<int:card_id>', methods=['GET', 'PUT', 'DELETE'])
def card_by_id(card_id):
    if request.method == 'GET':
        card = Card.query.get(int(card_id))
        if (card):
            return jsonify(card = card.serialize)
        else:
            return abort(404)
    elif request.method == 'PUT':
        card = Card.query.get(int(card_id))
        content = request.form.get('content')
        if (card):
            if (content):
                card.content = content
            db.session.commit()
            return make_response(("Card modified.", 200, None))
        else:
            return abort(404)

    elif request.method == 'DELETE':
        card = Card.query.get(int(card_id))
        if (card):
            db.session.delete(card)
            db.session.commit()
            return make_response(("Card deleted.", 200, None))
        elif (card is None):
            return make_response(("No card found.", 204, None))
    else:
        pass

