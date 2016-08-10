import datetime

from bson.objectid import ObjectId
from flask import request

from flongo import db_flongo


def check_for_session(session=None):
    # token is the ID of the user's current valid session
    token = request.cookies.get('Flongie')
    if token:
        current_time = datetime.datetime.now()
        session = db_flongo.sessions.find_one({'_id': ObjectId(token),
                                               'expiresOn': {'$gt': current_time}
                                               })
    return session


def archive_user_session(username, logout=False):
    last_session = db_flongo.sessions.find_one({'username': username}, {'_id': 0})
    if last_session:
        last_session['loggedOut'] = logout
        db_flongo.past_sessions.insert(last_session)
        db_flongo.sessions.remove({'username': username})
