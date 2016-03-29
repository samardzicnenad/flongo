from flongo import app
from flask import render_template, request


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return render_template('dummy.html')
    else:
        return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return render_template('dummy.html')
    else:
        return render_template('login.html')


@app.route('/error', methods=['GET', 'POST'])
def error():
    if request.method == 'POST':
        pass
    else:
        return render_template('error.html')