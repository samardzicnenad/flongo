import hashlib
import random
import re

from flongo import db_flongo
from globals import global_salt, bullet_separator


def user_validation(username, password, confirmation=None, email=None):
    # simple regex rules to validate user's data
    username_regex = re.compile(r'^[a-zA-Z][a-zA-Z0-9_-]{5,19}$')
    password_regex = re.compile(r'^.{8,20}$')
    email_regex = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
    errors = {}

    if not username_regex.match(username):
        errors['username'] = 'Invalid username{0}! ' \
                             'Your username must start with a character; ' \
                             'it can contain only characters, digits, underscore and/or dash symbols ' \
                             'and its length has to be between 6 and 20!'. \
                             format(wrap_invalid_element(username))

    if not password_regex.match(password):
        errors['password'] = 'Invalid password{0}! ' \
                             'Your password\'s length has to be between 8 and 20!'. \
                             format(wrap_invalid_element(password))

    if confirmation is not None and password != confirmation:
        errors['confirmation'] = 'Invalid password confirmation{0}! ' \
                                 'Your confirmation has to match the password!'. \
                                 format(wrap_invalid_element(confirmation))

    if email is not None and not email_regex.match(email):
        errors['email'] = 'Invalid email address{0}! ' \
                          'Your email address has to follow the pattern: local_part@domain_name.domain_extension !'. \
                          format(wrap_invalid_element(email))
    # return an array containing validation error messages
    return errors


def wrap_invalid_element(element):
    return ' ({0})'.format(element) if element else ''


def signup_user(username, password, email):
    user_salt = generate_user_salt()
    user_hash = generate_user_hash(global_salt, user_salt, password)
    user = {
        'username': username,
        'email': email,
        'user_salt': user_salt,
        'user_hash': user_hash
    }

    error_message = []
    try:
        db_flongo.users.insert(user)
    except Exception as ex:
        exception_type = type(ex).__name__
        # username and email address have to be unique (DB constraint)
        if exception_type == 'DuplicateKeyError':
            for element in ['email', 'username']:
                if element in ex.message:
                    msg = 'There is already a user with that {0}! Please, choose a different one!'.format(element)
                    error_message.append('{0}!{1}{2}'.format(exception_type, bullet_separator, msg))
        else:
            error_message.append('{0}!'.format(exception_type))
    return error_message


def generate_user_salt(length=64):
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(-_=+)'
    return ''.join(random.choice(chars) for _ in range(length))


def generate_user_hash(glob_salt, salt, password):
    return hashlib.sha512('{0}{1}{2}'.format(glob_salt, salt, password)).hexdigest()
