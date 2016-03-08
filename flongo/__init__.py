import os
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

import flongo.views

mongo_client = MongoClient(os.environ['MONGO_PORT_27017_TCP_ADDR'], 27017)
db = mongo_client.flongodb
