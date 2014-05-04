#!.venv/bin/python

import os
from flask import Flask, request, jsonify, abort, make_response, json
from app import app, db
from app import models
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
                               content = content,
                               userFirst = author.firstName,
                               userLast = author.lastName,
                               popularity = 0)
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
        return cors_response(("Card not found",400))

@app.route('/deku/api/cards/<int:card_id>', methods=['GET'])
def card_by_id(card_id):
    if request.method == 'GET':
        card = Card.query.get(int(card_id))
        if (card):
            return jsonify(card = card.serialize)
        else:
            return abort(404)
    else:
        pass

@app.route('/deku/api/cards/update/<int:card_id>', methods=['POST'])
def update_card(card_id):
    if request.method == 'POST':
        card = Card.query.get(int(card_id))
        content = request.form.get('content')
        if (card):
            if (content):
                card.content = content
            db.session.commit()
            return cors_response(("Card modified.", 200, None))
        else:
            return abort(404)
    else:
        pass

@app.route('/deku/api/cards/delete/<int:card_id>', methods=['POST'])
def delete_card(card_id):
    if request.method == 'POST':
        card = Card.query.get(int(card_id))
        author_id = card.user_id
        author = models.User.query.get(author_id) #get the author id from db
        password = request.form.get('password') # get password that was passed back
        user = authenticate_by_id(author_id, password) # just make sure the user is good
        if (user):
            if (card):
                db.session.delete(card)
                db.session.commit()
                return cors_response(("Card deleted.", 200, None))
            elif (card is None):
                return cors_response(("No card found.", 204, None))
        else:
            return cors_response(("Unauthorized access", 401))
    else:
        pass

@app.route('/deku/api/cards/profile/<int:user_id>', methods=['GET'])
def get_users_cards(user_id):
    if request.method == 'GET':
        hand = Card.query.filter(Card.user_id == user_id).all()
        addedCards = models.User.query.get(int(user_id)).addedCards
        for card in addedCards:
            if card in hand:
                pass
            else:
                hand.append(card)
        if len(hand) == 0:
            return cors_response(("No cards from user.", 204))
        return cors_response((jsonify(cards = [card.serialize for card in hand]), 200))
    else:
        pass

@app.route('/deku/api/cards/search/category/<category>', methods=['GET'])
def search_by_category(category):
    if request.method == 'GET':
        matches = Card.query.filter_by(category=category).all()
        if len(matches) == 0:
            return cors_response(("No matching cards.", 204))
        return cors_response((jsonify(cards = [card.serialize for card in matches]), 200))
    else:
        pass

@app.route('/deku/api/cards/search/tag/<tag>', methods=['GET'])
def search_by_tag(tag):
    if request.method == 'GET':
        matches = Card.query.filter(models.Card.tags.contains(tag)).all()
        if len(matches) == 0:
            return cors_response(("No matching cards.", 204))
        return cors_response((jsonify(cards = [card.serialize for card in matches]), 200))
    else:
        pass

@app.route('/deku/api/cards/search/author/<author>', methods=['GET'])
def search_by_author(author):
    if request.method == 'GET':
        firstName, lastName = author.split(",")
        matches = Card.query.filter(Card.userFirst == firstName and Card.userLast == lastName).all()
        if len(matches) == 0:
            return cors_response(("No matching cards.", 204))
        return cors_response((jsonify(cards = [card.serialize for card in matches]), 200))
    else:
        pass

@app.route('/deku/api/cards/add/<int:card_id>', methods=['POST'])
def addCardToDeck(card_id):
    if request.method == 'POST':
        # Verify card existence:
        card = models.Card.query.get(int(card_id))
        if (card):
            user_id = request.form.get("user_id")
            if (user_id):
                user = models.User.query.get(int(user_id))
                if (user):
                    if card in user.addedCards:
                        user.addedCards.remove(card)
                        card.popularity-=2
                    else:
                        user.addedCards.append(card)
                        card.popularity+=2
                        # Only notify the author if a user adds it. Unadding is not important
                        card_author = models.User.query.get(int(card.user_id)) #this is the user who authored the card
                        if (int(user_id) != card_author.id):
                            notification = models.Notification(from_id = user_id,
                                                               card_id = card_id,
                                                               content = "added")
                            card_author.notifications.append(notification) # append notification to user's account
                    db.session.commit()
                    return cors_response((jsonify(card.serialize), 200))
                else:
                    return cors_response(("User does not exist.", 404))
            else:
                return cors_response(("Bad request.", 400))
        else:
            return cors_response(("Card doesn't exist.", 404))
    else:
        pass

@app.route('/deku/api/cards/mark/<int:card_id>', methods=['POST'])
def markCard(card_id):
    if request.method == 'POST':
        # Verify card existence:
        card = models.Card.query.get(int(card_id))
        if (card):
            user_id = request.form.get("user_id")
            if (user_id):
                user = models.User.query.get(int(user_id))
                if (user):
                    # If card is already marked, remove it.
                    if card in user.markedCards:
                        user.markedCards.remove(card)
                        card.popularity-=1; # less popular
                    else:
                        user.markedCards.append(card)
                        print "pop: ", card.popularity
                        card.popularity+=1 # more popular
                        # Only notify the author if a user marks it. Unmarking is not important
                        card_author = models.User.query.get(int(card.user_id)) #this is the user who authored the card
                        if (int(user_id) != card_author.id):
                            notification = models.Notification(from_id = user_id,
                                                               card_id = card_id,
                                                               content = "marked")
                            card_author.notifications.append(notification) # append notification to user's account
                    db.session.commit()
                    return cors_response((jsonify(card.serialize), 200))
                else:
                    return cors_response(("User does not exist.", 404))
            else:
                return cors_response(("Bad request.", 400))
        else:
            return cors_response(("Card doesn't exist.", 404))
    else:
        pass
                  
@app.route('/deku/api/cards/comment/<int:card_id>', methods=['POST'])
def commentCard(card_id):
    if request.method == 'POST':
        # Verify card existence:
        card = models.Card.query.get(int(card_id))
        if (card):
            # set up data fields for comment
            author_id = request.form.get('author_id')
            content = request.form.get('content')
            comment = models.Comment(author_id = author_id,
                                     card_id = card_id,
                                     content = content)
            card.comments.append(comment)
            card.popularity+=1 # commenting is +1 popularity
            user = models.User.query.get(int(card.user_id)) #this is the user who authored the card
            # This is so a user doesn't get notification if they comment on their own card
            if (int(author_id) is not user.id):
                notification = models.Notification(from_id = author_id,
                                                   card_id = card_id,
                                                   content = "commented on")
                user.notifications.append(notification) # append notification to user's account
            db.session.commit()
            return cors_response((jsonify(card.serialize), 200))
        else:
            return cors_response(("Card doesn't exist.", 404))
    else:
        pass
                  
@app.route('/deku/api/cards/comment/delete/<int:card_id>', methods=['POST'])
def deleteComment(card_id):
    if request.method == 'POST':
        # Verify card existence:
        card = models.Card.query.get(int(card_id))
        if (card):
            # set up data fields for comment
            comment_id = request.form.get('comment_id')
            comment = models.Comment.query.get(comment_id)
            if (comment):
                card.comments.remove(comment)
                card.popularity-=1 # removing comment reduces popularity
                db.session.commit()
                return cors_response((jsonify(card.serialize), 200))
            else:
                return cors_response(("Comment doesn't exist", 404))
        else:
            return cors_response(("Card doesn't exist.", 404))
    else:
        pass
                
@app.route('/deku/api/cards/joker/<int:card_id>', methods=['POST'])
def setJoker(card_id):
    if request.method == 'POST':
        # Verify card existence:
        card = models.Card.query.get(int(card_id))
        if card:
            # Get user that reported the card.
            user_id = request.form.get('reporter_id')
            if (user_id):
                user = models.User.query.get(int(user_id))
                if (user):
                    if card in user.jokers:
                        return cors_response(("User cannot report card again.", 403))
                    user.jokers.append(card)

                    # Decrease popularity and alert admins, mods
                    if card.popularity >= 5:
                        card.popularity -= 5
                    else:
                        card.popularity = 0
                    
                    admins = models.User.query.filter_by(role=2).all()
                    # Append mods to admin list.
                    admins += models.User.query.filter_by(role=1).all()

                    for person in admins:
                        notification = models.Notification(from_id = user_id,
                                                           card_id = card_id,
                                                           content = "spotted a Joker on")
                        person.notifications.append(notification)
                    db.session.commit()
                    return cors_response((jsonify(card.serialize), 200))
                else:
                    return cors_response(("User not found.", 404))
            else:
                return cors_response(("Bad Request.", 400))
        else:
            return cors_response(("Card not found.", 404))
    else:
        pass  

@app.route('/deku/api/cards/hidden/<int:card_id>', methods=['POST'])
def hideCard(card_id):
    if request.method == 'POST':
        card = models.Card.query.get(int(card_id))
        if card:
            user_id = request.form.get('user_id')
            if user_id:
                user = models.User.query.get(int(user_id))
                if user:
                    if card in users.hiddenCards:
                        users.hiddenCards.remove(card)
                    else:
                        users.hiddenCards.append(card)
                    db.session.commit()
                    return cors_response((jsonify(user.serialize), 200))
                else:
                    return cors_response(("User not found.", 404))
            else:
                return cors_response(("Bad Request.", 400))
        else:
            return cors_response(("Card not found.", 404))
    else:
        pass
