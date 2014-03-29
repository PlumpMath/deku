#!/usr/bin/env python
import os
from flask import Flask, request, jsonify
from app import app, db, models

@app.route('/deku/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return jsonify(users = [user.serialize for user in models.User.query.all()])
    elif request.method == 'POST':
        # TODO check email passed for uniqueness
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        if (firstName and lastName and email):
            user = models.User(firstName = firstName,
                               lastName = lastName,
                               email = email)
            db.session.add(user)
            db.session.commit()
            return "New user added to database.\n"
        else:
            return "Wrong args passed.\n"
    else:
        pass

@app.route('/deku/api/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_by_id(user_id):
    if request.method == 'GET':
        user = models.User.query.get(int(user_id))
        if (user):
            return jsonify(id=user.id, firstName=user.firstName,
                    lastName=user.lastName, email=user.email)
        else:
            return "User %d not found.\n" % (user_id)
    elif request.method == 'PUT':
        user = models.User.query.get(int(user_id))
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        if (user):
            if (firstName):
                user.firstName = firstName
            if (lastName):
                user.lastName = lastName
            if (email):
                user.email = email
            db.session.commit()
            return "User %d updated.\n" % (user_id)
        else:
            return "User %d not found.\n" % (user_id)

    elif request.method == 'DELETE':
        user = models.User.query.get(int(user_id))
        if (user):
            db.session.delete(user)
            db.session.commit()
            return "User %d deleted.\n" % (user_id)
        else:
            return "User %d not found.\n" % (user_id)
    else:
        pass

@app.route('/deku/api/cards', methods=['GET', 'POST'])
def cards():
    if request.method == 'GET':
        return jsonify(cards = [card.serialize for card in models.Card.query.all()])
    elif request.method == 'POST':
        content = request.form.get('content')
        if (content):
            card = models.Card(content = content)
            db.session.add(card)
            db.session.commit()
            return "New card added to database.\n"
        else:
            return "Wrong args passed.\n"
    else:
        pass

@app.route('/deku/api/cards/<int:card_id>', methods=['GET', 'PUT', 'DELETE'])
def card_by_id(card_id):
    if request.method == 'GET':
        card = models.Card.query.get(int(card_id))
        if (card):
            return jsonify(content=card.content, author_id=card.user_id)
        else:
            return "Card %d not found.\n" % (card_id)
    elif request.method == 'PUT':
        card = models.Card.query.get(int(card_id))
        content = request.form.get('content')
        if (card):
            if (content):
                card.content = content
            db.session.commit()
            return "Card %d updated.\n" % (card_id)
        else:
            return "Card %d not found.\n" % (card_id)

    elif request.method == 'DELETE':
        card = models.Card.query.get(int(card_id))
        if (card):
            db.session.delete(card)
            db.session.commit()
            return "Card %d deleted.\n" % (card_id)
        else:
            return "Card %d not found.\n" % (card_id)
    else:
        pass

if __name__ == "__main__":
    app.run(debug=True)

