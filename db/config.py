#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# mysql db info
dbuser='root'
dbpass='pass'
dbname='db'
dbhost='localhost'
DB_URI = 'mysql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' + dbname + '?charset=utf8'

engine = create_engine(DB_URI, encoding='utf8')
DBSession = sessionmaker(bind=engine)


#trash code, just messing with MySQLdb
#import MySQLdb
#db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpass, charset="utf8")
#
#c = db.cursor()

#user_table = """CREATE TABLE IF NOT EXISTS `user`(
    #`id` int
    #`username`
    #`email`
    #`password`
    #`created`
#
    #id = Column(Integer, primary_key=True, nullable=False)
    #username = Column(Unicode(50,collation='utf8_bin'), unique=True, nullable=False)
    #email = Column(String(50), unique=True, nullable=False)
    #password = Column(Unicode(100,collation='utf8_bin'), nullable=False)
    #created = Column(DateTime, default=datetime.utcnow)


