import os
import flask
from pymongo import MongoClient

app = flask.Flask(__name__)

import flongo.views

mongo_client = MongoClient(os.environ['MONGO_PORT_27017_TCP_ADDR'], 27017)
db = mongo_client.flongodb