#!.venv/bin/python

import os
from flask import Flask, request, jsonify, abort, make_response, json
from app import app, db, session
from app import models
from app.models import Card
from utils import cors_response, authenticate
from flask.views import MethodView


@app.route('/deku/api/cards/search/<tag>', methods=['GET'])
def search_single_tag(tag):
    #results = db.session.query(models.Tag,models.Card).join(models.Card, models.Tag.card_id==models.Card.id).all()
    results = db.session.query(models.Tag,models.Card).filter(models.Tag.tag==tag).outerjoin(models.Card, models.Tag.card_id==models.Card.id).all()
    cards=[]
    for result in results:
        cards.append(result[1].serialize)
    return cors_response((jsonify(cards=cards),200))



class CardAPI(MethodView):
    def get(self, card_id):
        if card_id is None:
            return cors_response((jsonify(cards = [card.serialize for card in Card.query.all()]),200))
        else:
            card = Card.query.get(int(card_id))
            if (card):
                return jsonify(card = card.serialize)
            else:
                return cors_response(("Invalid Request",400))

    #modify user info
    #email, password, firstName, lastName, university, grad_year, major, classes[], bio 
    def post(self):
        if "user" not in session:
            return cors_response(("Unauthorized Access. Login to post a card",401))
        
        content = request.form.get('content')
        category = request.form.get('category')
        tags = request.form.getlist('tags')
        if (content):
            card = models.Card(user_id=session['user'].get('id'),content=content)
            if (category):
                card.category = category
            for tag in tags:
                card.tags.append(models.Tag(tag=tag))
            db.session.add(card)
            db.session.commit()
            return cors_response((jsonify(card = card.serialize), 201))
        else:
            return cors_response(("invalid request",400))

    def delete(self, card_id):
        if 'user' in session:
            card = Card.query.get(int(card_id))
            if not card:
                return cors_response(("Invalid request", 400))
            
            if card.user_id == session['user'].get('id') or \
                        session['user'].get('role') == models.ROLE_ADMIN:
                db.session.delete(card)
                db.session.commit()
                return cors_response(("Card deleted.", 200))
            else:
                return cors_response(("Invalid request 1", 400))
        else:
            return cors_response(("Unauthorized Access",401))

    def put(self, card_id):
        if 'user' in session:
            card = Card.query.get(int(card_id))
            if card:
                if card.user_id == session['user'].get('id') or \
                        session['user'].get('role')==models.ROLE_ADMIN:
                    content = request.form.get('content')
                    if content:
                        card.content = content
                        db.session.commit()
                    return cors_response(('Card modified',200))
                else:
                    return cors_response(('Invalid Request',400))
            else:
                return cors_response(('Invalid Request 1',400))
        else:
            return cors_response(("Unauthorized Access",401))

card_view = CardAPI.as_view('card_api')
app.add_url_rule('/deku/api/cards', defaults={'card_id': None},
                 view_func=card_view, methods=['GET',])
app.add_url_rule('/deku/api/cards', view_func=card_view, methods=['POST',])
app.add_url_rule('/deku/api/cards/<int:card_id>', view_func=card_view,
                 methods=['GET', 'PUT', 'DELETE'])


