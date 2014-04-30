from flask import Flask, session
from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.bcrypt import Bcrypt
import os

app = Flask(__name__)
app.secret_key = os.urandom(777)
app.config.from_object('config')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Initialize Pydenticon service.
import pydenticon
import hashlib

# Foreground colors:
foreground = ["rgb(45,79,255)",
              "rgb(254,180,44)",
              "rgb(226,121,234)",
              "rgb(30,179,253)",
              "rgb(232,77,65)",
              "rgb(49,203,115)",
              "rgb(141,69,170)" ]
# Background colors:
background = "rgb(224,224,224)"

# Instantiate generator:
generator = pydenticon.Generator(5, 5, digest=hashlib.sha1,
                                 foreground=foreground, 
                                 background=background)

import models
import users
import cards
import admin
import messages
