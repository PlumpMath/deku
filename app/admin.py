#!.venv/bin/python

import os
from flask import Flask, request, jsonify, abort, render_template, json
from sqlalchemy.orm import subqueryload, contains_eager
from app import app, db, models, bcrypt, session
from utils import cors_response, authenticate_by_email, authenticate_by_id

@app.route('deku/api/admin/users/make_moderator/<int:user_id>', methods=['PUT'])
def makeModerator():
    pass

@app.route('deku/api/admin/users/delete/<int:user_id>', methods=['DELETE'])
def deleteUser():
    pass
