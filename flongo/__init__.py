import os

import flask
import sassutils.wsgi
from pymongo import MongoClient

app = flask.Flask(__name__)

mongo_client = MongoClient(os.environ['MONGO_PORT_27017_TCP_ADDR'], 27017)
db_flongo = mongo_client.flongo

db_flongo.users.create_index('username', unique=True)
db_flongo.users.create_index('email', unique=True)

db_flongo.sessions.create_index('username')
db_flongo.sessions.create_index('expiresOn')

import flongo.views

app.wsgi_app = sassutils.wsgi.SassMiddleware(app.wsgi_app, {
    'flongo': ('static/sass', 'static/css', '/static/css')
})
