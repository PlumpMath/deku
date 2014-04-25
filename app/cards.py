#!.venv/bin/python

import os
from flask import Flask, request, jsonify, abort, make_response, json
from app import app, db, session
from app import models
from app.models import Card
from utils import cors_response
from flask.views import MethodView
from sqlalchemy import and_
from utils import validate_user


@app.route('/deku/api/cards/<int:card_id>/mark', methods=['PUT','POST'])
def mark_card(card_id):
    id = validate_user()
    mark = models.Mark.query.filter(and_(models.Mark.user_id==id, models.Mark.card_id==card_id)).first()
    if mark is None:
        db.session.add(models.Mark(user_id=id, card_id=card_id))
        db.session.commit()
        return cors_response(("Mark added",200))
    else:
        return cors_response(("Mark already exists",200))
    
@app.route('/deku/api/cards/<int:card_id>/unmark', methods=['PUT','POST'])
def unmark_card(card_id):
    id = validate_user()
    mark = models.Mark.query.filter(and_(models.Mark.user_id==id, models.Mark.card_id==card_id)).first()
    if mark is None:
        return cors_response(("No mark to removeadded",200))
    else:
        db.session.delete(mark)
        db.sessoin.commit()
        return cors_response(("Mark removed",200))

@app.route('/deku/api/cards/search/user/<user_id>', methods=['GET'])
def search_by_user(user_id):
    cards = db.session.query(models.Card).filter(models.Card.user_id==user_id).order_by(models.Card.id).limit(20).all()
    return cors_response((jsonify(cards=[card.serialize for card in cards]),200))    

#get last 20 cards with <tag>
@app.route('/deku/api/cards/search/tag/<tag>', methods=['GET'])
def search_by_tag(tag):
    results = db.session.query(models.Tag,models.Card).filter(models.Tag.tag==tag).outerjoin(models.Card, models.Tag.card_id==models.Card.id).order_by(models.Tag.id).limit(20).all()
    cards=[]
    for result in results:
        cards.append(result[1].serialize)
    return cors_response((jsonify(cards=cards),200))

@app.route('/deku/api/cards/delete/<int:card_id>',methods=['POST','PUT'])
def delete_card(card_id):
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


#used by post and put
def update_fields(card):
    content = request.form.get('content')
    category = request.form.get('category')
    tags = request.form.getlist('tags[]')
    print tags
    comments = request.form.getlist('comments')
    date = request.form.get('date')
    time = request.form.get('time')
    if content:
        card.content = content
    if category:
        card.category = category
    if tags:
        card.tags2 = ",".join(tags)
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
        print request.form
        print request.form
        id = validate_user()
        if id:
            card = models.Card(user_id = id)
            update_fields(card)
            db.session.add(card)
            db.session.commit()
            return cors_response((jsonify(card = card.serialize), 201))
        else:
            return cors_response(("Unauthorized Access",401))


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
                 methods=['GET', 'PUT'])
