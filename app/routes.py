#!.venv/bin/python
import os
from flask import Flask, request, jsonify, abort, make_response
from app import app, db, models, bcrypt

@app.route('/deku/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return jsonify(users = [user.serialize for user in models.User.query.all()])
    elif request.method == 'POST':
        # TODO check email passed for uniqueness
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        if (firstName and lastName and email and password):
            pw_hash = bcrypt.generate_password_hash(password)
            user = models.User(firstName = firstName,
                               lastName = lastName,
                               email = email,
                               password = pw_hash)
            db.session.add(user)
            db.session.commit()
            return make_response(("User created.", 201, None))
        else:
            abort(400)
    else:
        pass

@app.route('/deku/api/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_by_id(user_id):
    if request.method == 'GET':
        user = models.User.query.get(int(user_id))
        if (user):
            return jsonify(user = user.serialize)
        else:
            abort(404)
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
            return jsonify(user = user.serialize)
        else:
            abort(404)

    elif request.method == 'DELETE':
        user = models.User.query.get(int(user_id))
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return make_response(("User deleted.", 200, None))
        else:
            return make_response(("No user found.", 204, None))
    else:
        pass

@app.route('/deku/api/users/login', methods=['POST'])
def user_authentication():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if (email and password):
            user = models.User.query.filter_by(email=email).first()
            if (user):
                correct_pw = bcrypt.check_password_hash(user.password, password)
                if (correct_pw):
                    return jsonify(user = user.serialize)
                else:
                    return make_response(("Email or password was invalid.", 401, None))
            else:
                return abort(404)
        else:
            return make_response(("Email or password missing.", 401, None))
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
            return make_response(('Card created.', 201, None))
        else:
            return abort(400)
    else:
        pass

@app.route('/deku/api/cards/<int:card_id>', methods=['GET', 'PUT', 'DELETE'])
def card_by_id(card_id):
    if request.method == 'GET':
        card = models.Card.query.get(int(card_id))
        if (card):
            return jsonify(card = card.serialize)
        else:
            return abort(404)
    elif request.method == 'PUT':
        card = models.Card.query.get(int(card_id))
        content = request.form.get('content')
        if (card):
            if (content):
                card.content = content
            db.session.commit()
            return make_response(("Card modified.", 200, None))
        else:
            return abort(404)

    elif request.method == 'DELETE':
        card = models.Card.query.get(int(card_id))
        if (card):
            db.session.delete(card)
            db.session.commit()
            return make_response(("Card deleted.", 200, None))
        elif (card is None):
            return make_response(("No card found.", 204, None))
    else:
        pass

if __name__ == "__main__":
    app.run(debug=True)
