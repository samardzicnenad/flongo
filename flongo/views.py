import datetime
from signal import signal, SIGPIPE, SIG_DFL

from flask import request, redirect, url_for, render_template

from flongo import app, db_flongo
from globals import global_salt, bullet_separator
from session import check_for_session, archive_user_session
from user import signup_user, generate_user_hash, user_validation

# attempt to prevent: "IOError: [Errno 32] Broken pipe"
signal(SIGPIPE, SIG_DFL)


@app.route('/', methods=['GET'])
def flongo():
    session = check_for_session()
    if session:
        return redirect(url_for('index', username=session['username']))
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        # retrieve user's signup data
        username = ignore_non_ascii(request.form['username'])
        password = ignore_non_ascii(request.form['password'])
        confirmation = ignore_non_ascii(request.form['confirmation'])
        email = ignore_non_ascii(request.form['email'])

        # ...and validate it
        validation_issues = user_validation(username, password, confirmation, email)

        if not validation_issues:
            signup_issues = signup_user(username, password, email)
            if not signup_issues:
                return render_template('welcome.html', username=username)
            else:
                # report signup issues
                return render_error_page(signup_issues, 'signup')
        else:
            return report_validation_issues('signup',
                                            ['username', 'password', 'confirmation', 'email'],
                                            validation_issues)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        # retrieve user's login data
        username = ignore_non_ascii(request.form['username'])
        password = ignore_non_ascii(request.form['password'])

        # ...and validate it
        validation_issues = user_validation(username, password)

        if not validation_issues:
            user = db_flongo.users.find_one({'username': username}, {'_id': 0, 'email': 0})
            # non existing user
            if not user:
                return render_error_page(['A user with the provided username does not exist! Please, try again.'],
                                         'login')

            user_salt = user['user_salt']
            user_hash = user['user_hash']
            check_hash = generate_user_hash(global_salt, user_salt, password)
            # wrong password
            if user_hash != check_hash:
                return render_error_page(['You provided an incorrect password! Please, try again.'], 'login')

            # create a user session
            created_on = datetime.datetime.now()
            expires_on = created_on + datetime.timedelta(minutes=30)
            session = {
                'username': username,
                'createdOn': created_on,
                'expiresOn': expires_on,
                'loggedOut': False
            }
            try:
                archive_user_session(username)
                _id = db_flongo.sessions.insert(session)
                response = redirect(url_for('index', username=username))
                response.set_cookie('Flongie', value=bytes(_id), max_age=30 * 60)
                return response
            except Exception as ex:
                return render_error_page([type(ex).__name__], 'login')
        else:
            return report_validation_issues('login',
                                            ['username', 'password'],
                                            validation_issues)


@app.route('/index', methods=['GET', 'POST'])
def index():
    session = check_for_session()
    if session:
        if request.method == 'GET':
            username = request.args.get('username')
            return render_template('index.html', username=username)
        else:
            username = request.form['username']
            archive_user_session(username, True)
            return redirect(url_for('flongo'))
    else:
        return redirect(url_for('login'))


def report_validation_issues(source, field_list, validation_issues):
    issues = ['There were problems validating your {0} data:'.format(source)]
    for element in field_list:
        if element in validation_issues:
            issues.append(validation_issues[element])
    return render_error_page(issues, source)


def render_error_page(errors, target):
    return render_template('error.html', errors=bullet_separator.join(errors), target=target)


def ignore_non_ascii(field):
    return field.encode('ascii', 'ignore').decode('ascii')


# auxiliary route - lists out existing users and current/past sessions
@app.route('/info', methods=['GET'])
def info():
    users = db_flongo.users.find()
    user_list = [user for user in users]
    sessions = db_flongo.sessions.find()
    session_list = [session for session in sessions]
    past_sessions = db_flongo.past_sessions.find()
    past_session_list = [past_session for past_session in past_sessions]
    return render_template('info.html', users=user_list, sessions=session_list, past_sessions=past_session_list)
