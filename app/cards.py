#!.venv/bin/python

import os
from flask import Flask, request, jsonify, abort, make_response, json
from app import app, db, models, session
from app.models import Card
from utils import cors_response, authenticate_by_email, authenticate_by_id

@app.route('/deku/api/cards', methods=['GET', 'POST'])
def cards():
    if request.method == 'GET':
        return cors_response((jsonify(cards = [card.serialize for card in models.Card.query.all()]), 200))

    elif request.method == 'POST':         
        content = request.form.get('content')
        category = request.form.get('category')
        tags = request.form.get('tags')
        author_id = request.form.get('author_id')
        author = models.User.query.get(author_id) #get the author id from db
        if (content):
            card = models.Card(user_id = author_id,
                               content=content,
                               userFirst = author.firstName,
                               userLast = author.lastName)
            if (category):
                card.category = category

            if (tags):
                tagList = json.loads(tags)
                card.tags = ",".join(tagList)

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

@app.route('/deku/api/cards/search/category/<category>', methods=['GET'])
def search_by_category(category):
    if request.method == 'GET':
        matches = models.Card.query.filter_by(category=category).all()
        if len(matches) == 0:
            return cors_response(("No matching cards.", 204))
        return cors_response((jsonify(card.serialize for card in matches), 200))
    else:
        pass

@app.route('/deku/api/cards/search/tag/<tag>', methods=['GET'])
def search_by_tag(tag):
    pass

@app.route('/deku/api/cards/search/author/<author>', methods=['GET'])
def search_by_author(author):
    pass
