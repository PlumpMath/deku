#!.venv/bin/python

import os
from flask import Flask, request, jsonify, abort, make_response, json
from app import app, db, session
from app import models
from app.models import Card
from utils import cors_response, authenticate
from flask.views import MethodView

@app.route('/deku/api/cards/<int:card_id>/comments',methods=['GET'])
def getAll(card_id):
    return CommentAPI().getAll(card_id)

@app.route('/deku/api/cards/<int:card_id>/comments',methods=['POST'])
def addComment(card_id):
    comment = request.form.get('comment')
    return CommentAPI().addComment(card_id,comment)

@app.route('/deku/api/cards/<int:card_id>/comments/<int:comment_id>',methods=['GET','PUT','DELETE'])
def deku_api_cards_cardId_comments_commentId(card_id,comment_id=None):
    return cors_response(("Other stuff to implement",400))
    #remaining = path.split('/')
    #print remaining
    #if request.method=='GET':
    #print request.method
    
    #card = models.Card.query.get(card_id)
    #if card:
        #comment = request.form.get('comment')
        #if not comment_id:
            #if request.method=='POST':
                #if(comment):
                    #something = CommentAPI().add_comment(comment)
                    #print something
                    #return something
                #else:
                    #return cors_response(("No comment to post",400))
            #elif request.method=='GET':
                #return CommentAPI().getAll()
    #else:
        #return cors_response(("Invalid Request. No such card.",400))

    #return cors_response(("Invalid Request",400))

class CommentAPI():
    def addComment(self, card_id, comment):
        if 'user' in session:
            card = Card.query.get(int(card_id))
            if card:
                comment = request.form.get('comment')
                if comment:
                    tmpComment = models.Comment()
                    tmpComment.user_id = session['user'].get('id')
                    tmpComment.card_id = card_id
                    tmpComment.comment = comment
                    db.session.add(tmpComment)
                    db.session.commit()
                return cors_response((jsonify(comment=tmpComment.serialize),201))
            else:
                return cors_response(('Invalid Request 1',400))
        else:
            return cors_response(("Unauthorized Access",401))
        return cors_response(("Invalid final",400))
    def getAll(self, card_id):
        comments = models.Comment.query.filter(models.Comment.card_id==card_id).all()
        return cors_response((jsonify(comments=[comment.serialize for comment in comments])))

    def delete(self, card_id):
        pass
    
    def put(self, card_id):
        pass



