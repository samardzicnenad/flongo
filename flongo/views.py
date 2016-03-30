from flongo import app
from flask import render_template, request


@app.route('/', methods=['GET'])
def welcome():
    return render_template('welcome.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        pass
    else:
        return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass
    else:
        return render_template('login.html')


@app.route('/dummy', methods=['GET', 'POST'])
def dummy():
    if request.method == 'GET':
        pass
    else:
        return render_template('dummy.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pass
    else:
        return render_template('index.html')


@app.route('/error', methods=['GET', 'POST'])
def error():
    if request.method == 'POST':
        pass
    else:
        return render_template('error.html')
