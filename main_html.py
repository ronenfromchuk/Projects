import uuid
import flask
from flask import Flask, render_template, request, session, url_for, request
from Users import Users
from DbRepo import DbRepo
from db_config import local_session
from werkzeug.security import generate_password_hash, check_password_hash

repo = DbRepo(local_session)
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


# localhost:5000/
@app.route("/")
def home():
    try:
        if session['remember'] == 'on': return flask.redirect(url_for('login_success'))
    except: pass
    return flask.redirect(url_for('login'))

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', try_again=False, registered_success=False)

@app.route('/my_app', methods=['GET'])
def login_success():
    try:
        user = repo.get_by_column_value(Users, Users.username, session['uname'])
        if user[0] != None: return render_template('my_app.html') 
    except: pass
    return render_template('login.html', try_again=True, registered_success=False)

@app.route('/login_process', methods=['POST'])
def hanle_login():
    form_data = request.form
    username = form_data.get('uname')
    password = form_data.get('psw')
    print(request)
    print(form_data)
    try: 
        user = repo.get_by_column_value(Users, Users.username, username)
        if username == user[0].username and check_password_hash(user[0].password, password): 
            session['remember'] = request.form.get('remember')
            session['uname'] = username
            session['pwd'] = password if session['remember'] == 'on' else None
            return flask.redirect(url_for('login_success'))
    except: pass
    return render_template('login.html', try_again=True)

@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html', bad_repeat=False, user_exists=False, email_exists=False, short_password=False)

@app.route('/signup_process', methods=['POST'])
def handle_signup():
    if request.form['psw'] != request.form['psw-repeat']: return render_template('signup.html', bad_repeat=True)
    form_data = request.form

    username = form_data.get('uname')
    password = form_data.get('psw')
    email = form_data.get('email')

    user_username = repo.get_by_column_value(Users, Users.username, username)
    user_email = repo.get_by_column_value(Users, Users.email, email)
    if user_username: return render_template('signup.html', bad_repeat=False, user_exists=True, email_exists=False, short_password=False, status=202, mimetype='application/json')
    elif user_email: return render_template('signup.html', bad_repeat=False, user_exists=False, email_exists=True, short_password=False, status=202, mimetype='application/json')
    elif len(password) < 6: return render_template('signup.html', bad_repeat=False, user_exists=False, email_exists=False, short_password=True, status=202, mimetype='application/json')
    else:
        repo.add(Users(username=username, password=generate_password_hash(password), email=email))
        return render_template('login.html', try_again=False, registered_success=True, status=201, mimetype='application/json')

@app.route('/logout', methods=['GET'])
def logging_out():
    session['remember'], session['uname'], session['pwd'] = None, None, None
    return flask.redirect(url_for('login'))

app.run(debug=True, port=5000)