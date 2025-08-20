import re
import os
from functools import wraps
from typing import Callable

from flask import Flask, request, redirect, render_template, session
import psycopg2
from psycopg2.extensions import connection as PGConnection
import bcrypt
from db import User, Ride

KEY = os.environ.get('KEY')
DB_URL = os.environ.get('DATABASE_URL', 'dbname=motus')

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')
app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config['SESSION_COOKIE_SECURE'] = True

# ------- Decorators ------- #
def get_database_connection(function: Callable):
    @wraps(function)
    def wrapper(*args, **kwargs):
        with psycopg2.connect(DB_URL) as conn:
            kwargs['conn'] = conn
            result = function(*args, **kwargs)
            conn.commit()
            return result
    return wrapper

def check_auth(function: Callable):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect('/login')
        return function(*args, **kwargs)
    return wrapper

# ------- Routes ------- #
@app.route('/')
def on_boarding():
    return render_template('on_boarding.html')

# ------- settings page ------- #
@app.route('/settings')
def settings():
    return render_template('settings.html')
    
# ------- Setting session/cookies ------- #   
@app.route('/user_info')
def method_name():
    username = session.get('username')
    return render_template('user.html', username=username)

# ------- User page ------- #
@app.route('/user')
@check_auth
def user():
    user_id = session.get('user_id')
    username = session.get('username')
    email = session.get('email')

    if not user_id or not username or not email:
        return redirect('/login')

    return render_template('user.html', user_id=user_id, username=username, email=email)

# ------- Login ------- #
@app.route('/login', methods=['POST', 'GET'])
@get_database_connection
def login(conn: PGConnection):
    if request.method == 'GET':
        return render_template('login.html')
    
    email = (request.form.get('email') or '').strip().lower()
    password = (request.form.get('password') or '')
    logged_in_user = User.get_user_via_email(email, conn)


    if not logged_in_user:
        print('Email or password is incorrect')
        return render_template('login.html', error='Email or password is incorrect.')

    hash_pw = logged_in_user.hash_pw.encode('utf-8') if isinstance(logged_in_user.hash_pw, str) else logged_in_user.hash_pw
    if bcrypt.checkpw(password.encode('utf-8'), hash_pw):
        print("Password matches")
        session['email'] = logged_in_user.email
        session['user_id'] = logged_in_user.user_id
        session['username'] = logged_in_user.username
        return redirect('/user_info')
    else:
        print("Password does not match")
        return render_template('login.html', error='Email or password is incorrect.')

# ------- Logout -------#
@app.route('/log_out')
@check_auth
def log_out():
    session.clear()
    return redirect('/')

# ------- User Info ------- #
@app.route('/user_info')
@check_auth
def user_info():
    user_id = session.get('user_id')
    username = session.get('username')
    email = session.get('email')

    if not user_id or not username or not email:
        return redirect('/login')

    return render_template('user.html', user_id=user_id, username=username, email=email)

# ------- Sign up ------- #
@app.route('/sign_up', methods=['POST', 'GET'])
@get_database_connection
def sign_up(conn: PGConnection):
    username = (request.form.get('username') or '').strip()
    email = (request.form.get('email') or '').strip().lower()
    password = (request.form.get('password') or '')

    if request.method == 'GET':
        print('GET request for sign up page')
        return render_template('sign_up_page.html')
    
    if not username or not email or not password:
        print('Username or password or email is empty')
        return render_template('sign_up_page.html', error='Username, email, and password are required.')
        
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        print("Invalid email format")
        return render_template('sign_up_page.html', error='Invalid email format.')

    hash_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = User(
        user_id=None,
        username=username,
        email=email,
    )
    user.hash_pw = hash_pw
    user.save(conn)

    if not user:
        print('User creation failed')
        return render_template('sign_up_page.html', error='User creation failed.')

    return redirect('/user')

# ------- Process rides ------- #
@app.route('/process_rides', methods=['POST', 'GET'])
@get_database_connection
def process_rides(conn: PGConnection):
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    if request.method == 'GET':
        return render_template('add_ride.html')
    
    ride_description = (request.form.get('ride_description') or '').strip()
    ride_start = (request.form.get('ride_start') or '').strip()
    ride_end = (request.form.get('ride_end') or '').strip()

    if not ride_description or not ride_start or not ride_end:
        return render_template('show_rides.html', error='All fields are required.')

    ride = Ride(
        ride_id=None,
        user_id=user_id,
        ride_description=ride_description,
        ride_start=ride_start,
        ride_end=ride_end
    )
    ride.save(conn)
    return redirect('/show_rides')

# ------- Displaying rides ------- #
@app.route('/show_rides')
@get_database_connection
def show_rides(conn: PGConnection):
    user_id = session.get('user_id')
    username = session.get('username')  
    rides = Ride.get_rides_for_user(user_id, conn)
    print(f"Rides for user {user_id}: {rides}")
    return render_template('show_rides.html' , KEY=KEY, rides=rides, username=username)

# ------- Delete rides ------- #
@app.route('/delete/<int:ride_id>', methods=['POST'])
@get_database_connection
def delete(ride_id, conn: PGConnection):
    Ride.delete_ride(ride_id, conn)
    return redirect('/show_rides')


if __name__ == "__main__":
    app.run(debug=True)