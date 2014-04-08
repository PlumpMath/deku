#!.venv/bin/python

import os
from flask import Flask, request, jsonify, abort, make_response, json
from app import app, db, models, session
from app.models import Card
from cors import crossdomain

@crossdomain(origin='*')
@app.route('/deku/api/cards', methods=['GET', 'POST'])
def cards():
    if request.method == 'GET':
        return jsonify(cards = [card.serialize for card in Card.query.all()])
    elif request.method == 'POST':
        if 'id' not in session:
            return make_response("Must be logged in to post a new card", 401)
        user = db.session.query(models.User).filter(models.User.id == session['id']).first()
        print user
        content = request.form.get('content')
        suit = request.form.get('suit')
        tags = request.form.get('tags')
        tags = json.loads(tags)
        print tags
        if (content):
            card = Card(user_id = id, content = content)
            if suit:
                card.suit = suit
            user.cards.append(card)
            for tag in tags:
                card.tags.append(models.Tag(tag))
            db.session.commit()
            return make_response((jsonify(card = card.serialize), 201))
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

