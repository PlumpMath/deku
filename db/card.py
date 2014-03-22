#!/usr/bin/env python

from datetime import datetime
from flask import jsonify
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, exc, desc
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from config import DBSession, Card, Tag
from user import getUser

#add cards and tags
def addCard(dbsession, user_id, category, content, tags):
    #user = getUser(dbsession, user_id)
    card = Card(user_id=user_id, category=category, content = content)
    for it in tags:
        card.tags.append(Tag(tag=it))
    print card.tags
    user = getUser(dbsession, user_id)
    user.cards.append(card)
    
#delete cards and rows in tags affecting only that card
def deleteCard(dbsession, card_id):
    card = dbsession.query(Card).filter(Card.id==card_id).first()
    if card is None:
        return 'Card already deleted'
    else:
        dbsession.delete(card)
        dbsession.commit()
        return 'Deleted'

#returns last x cards posted
def getLastCards(dbsession, numCards):
    cards = dbsession.query(Card).order_by(desc(Card.id)).limit(numCards)
    deck=[]
    for card in cards:
        c=card.toDict()
        deck.append(c)
    print c
    print vars(jsonify(c))
    return jsonify(c)
    
    
if __name__ == "__main__":
    dbsession = DBSession()
    cards = getLastCards(dbsession, 5)
    
    #card = Card(category='cat', content='faq')
    #card.tags.append(Tag())
    #dbsession.add(card)
    #card.tags.append(Tag(tag='faqin'))
    #card.tags.append(Tag(tag='heal'))
    #dbsession.commit()
    
    #tag = dbsession.query(Tag).filter(Tag.id==1).first()
    #print card
    #dbsession.delete(tag)
    #print card
    #dbsession.commit()
    #print card
    #dbsession.commit()