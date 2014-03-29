#!/usr/bin/env python
import os
from flask import Flask, request
from app import app

@app.route('/deku/api/users', methods=['GET'])
def users():
    if request.method == 'GET':
        return "Getting all users.\n"
    else:
        pass

@app.route('/deku/api/users/<int:user_id>', methods=['GET', 'POST', 'PUT',
    'DELETE'])
def user_by_id(user_id):
    if request.method == 'GET':
        return "Getting user with id " + str(user_id) + "\n"
    elif request.method == 'POST':
        return "Creating user with id " + str(user_id) + "\n"
    elif request.method == 'PUT':
        return "Changing info of user with id " + str(user_id) + "\n"
    elif request.method == 'DELETE':
        return "Deleting user with id " + str(user_id) + "\n"
    else:
        pass

@app.route('/deku/api/cards', methods=['GET'])
def cards():
    if request.method == 'GET':
        return "Getting all cards\n"
    else:
        pass

@app.route('/deku/api/cards/<int:card_id>', methods=['GET', 'POST', 'PUT',
'DELETE'])
def card_by_id(card_id):
    if request.method == 'GET':
        return 'Getting card with id ' + str(card_id) + "\n"
    elif request.method == 'POST':
        return "Creating card with id " + str(card_id) + "\n"
    elif request.method == 'PUT':
        return "Changing info of card with id " + str(card_id) + "\n"
    elif request.method == 'DELETE':
        return "Deleting card with id " + str(card_id) + "\n"
    else:
        pass

if __name__ == "__main__":
    app.run(debug=True)

