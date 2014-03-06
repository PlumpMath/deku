#!/usr/bin/env python
from sqlalchemy import create_engine

# mysql db info
dbuser='root'
dbpass='pass'
dbname='db'
dbhost='localhost'
DB_URI = 'mysql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' + dbname

engine = create_engine(DB_URI)

