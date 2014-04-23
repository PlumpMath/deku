#!.venv/bin/python

import os
from flask import Flask, request, jsonify, abort, make_response, json
from app import app, db, session
from app import models
from app.models import Card
from utils import cors_response
from flask.views import MethodView
from sqlalchemy import or_
from utils import validate_user

#get last 20 cards with <tag>
@app.route('/deku/api/cards/search/<tag>', methods=['GET'])
def search_single_tag(tag):
    results = db.session.query(models.Tag,models.Card).filter(models.Tag.tag==tag).outerjoin(models.Card, models.Tag.card_id==models.Card.id).order_by(models.Tag.id).limit(20).all()
    cards=[]
    for result in results:
        cards.append(result[1].serialize)
    return cors_response((jsonify(cards=cards),200))


def update_fields(card):
    content = request.json.get('content')
    category = request.json.get('category')
    tags = request.json.get('tags')
    comments = request.json.get('comments')
    date = request.json.get('date')
    time = request.json.get('time')
    if content:
        card.content = content
    if category:
        card.category = category
    if tags:
        for tag in tags:
            card.tags.append(models.Tag(tag=tag))
    if comments:
        for comment in comments:
            card.comments.append(models.Comment(comment = comment))
    if time:
        card.time = time
    if date:
        card.date = date
        
class CardAPI(MethodView):
    def get(self, card_id):
        if card_id is None:
            return cors_response((jsonify(cards = [card.serialize for card in Card.query.order_by(models.Card.id.desc()).limit(20).all()]),200))
        else:
            card = Card.query.get(int(card_id))
            if (card):
                return jsonify(card = card.serialize)
            else:
                return cors_response(("Invalid Request",400))

    #modify user info
    #email, password, firstName, lastName, university, grad_year, major, classes[], bio
    def post(self):
        id = validate_user()
        if id:
            card = models.Card(user_id = id)
            update_fields(card)
            db.session.add(card)
            db.session.commit()
            return cors_response((jsonify(card = card.serialize), 201))
        else:
            return cors_response(("Unauthorized Access",401))


    def delete(self, card_id):
        card = Card.query.get(int(card_id))
        if not card:
            return cors_response(("Invalid request", 400))


        if card:
            if validate_user(card.user_id):
                db.session.delete(card)
                db.session.commit()
                return cors_response(("Card deleted.",200))
            else:
                return cors_response(("Unauthorized Access",401))
        else:
            return cors_response(("Card not found",400))

    #if card belongs to the json.request.get('user') and json.request.get('pwd')
    def put(self, card_id):
        card = Card.query.get(int(card_id))
        if card:
            if validate_user(card.user_id):
                models.Tag.query.filter(models.Tag.card_id==card.id).delete()
                models.Comment.query.filter(models.Comment.card_id==card.id).delete()
                update_fields(card)
                db.session.commit()
                return cors_response((jsonify(card = card.serialize),200))
            else:
                return cors_response(("Unauthorized Access",401))
        else:
            return cors_response(("Card not found",400))

card_view = CardAPI.as_view('card_api')
app.add_url_rule('/deku/api/cards', defaults={'card_id': None},
                 view_func=card_view, methods=['GET',])
app.add_url_rule('/deku/api/cards', view_func=card_view, methods=['POST',])
app.add_url_rule('/deku/api/cards/<int:card_id>', view_func=card_view,
                 methods=['GET', 'PUT', 'DELETE'])