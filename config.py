import os
basedir = os.path.abspath(os.path.dirname(__file__))

USERNAME = "admin"
PASSWORD = "password"
SERVER = "localhost"
SQLALCHEMY_DATABASE_URI = 'mysql://' + USERNAME + ":" + PASSWORD + "@" + SERVER + "/db"
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
