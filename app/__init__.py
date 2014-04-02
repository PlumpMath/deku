from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config.from_object('config')
app.secret_key=os.urandom(777)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
logged_in=dict()

import models
import routes
