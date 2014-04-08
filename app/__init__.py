from flask import Flask, session
from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.bcrypt import Bcrypt
import os

app = Flask(__name__)
app.secret_key = os.urandom(777)
app.config.from_object('config')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

import models
import users
import cards
