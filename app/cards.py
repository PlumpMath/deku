#!.venv/bin/python

import os
from flask import Flask, request, jsonify, abort, make_response
from app import app, db
from app.models import Card
from cors import crossdomain

@crossdomain(origin='*')
@app.route('/deku/api/cards', methods=['GET', 'POST'])
def cards():
    if request.method == 'GET':
        return jsonify(cards = [card.serialize for card in Card.query.all()])
    elif request.method == 'POST':
        content = request.form.get('content')
        if (content):
            card = Card(content = content)
            db.session.add(card)
            db.session.commit()
            return make_response(('Card created.', 201, None))
        else:
            return abort(400)
    else:
        pass

@crossdomain(origin='*')
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

