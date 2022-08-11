from crypt import methods
import re
from flask import Flask, request,  redirect, render_template, session, flash 
import os 
import psycopg2
import bcrypt

KEY = 'ApcKaohzYrX3IDg_HAIT1e4j5xfiAO4c-4xLukmzExsOMFRxkNGkdYahxjC6owS6'
DB_URL = os.environ.get('DATABASE_URL','dbname=motus')
SECRET_KEY = os.environ.get('SECRET_KEY', 'pretend secret  KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def on_boarding():
        return render_template('on_boarding.html')

@app.route('/login_page')
def login_page():
    return render_template('login_page.html')

@app.route('/signUp_page' )
def signUp():
    return render_template('signUp_page.html')
# ------- login ------- #
@app.route('/login', methods=['POST'])
def login_action():
    email = request.form.get('email')
    password = request.form.get('password')
    user_id = request.form.get('user_id')
    username = request.form.get('username')
    
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    cur.execute("SELECT email, hash_pw, user_id, username FROM motus_users WHERE email = %s", [email])
    results = cur.fetchone()
    print(results)
    conn.commit()
    conn.close()
    
    #if email is not in results the return login page
    if results[0] and results[1] == None:
        
        # flash('You information is incorrect, try again')
        return redirect('/')
# ------- password checking ------- #
    if bcrypt.checkpw(password.encode(), results[1].encode()) == True and email == results[0]:
        session['email'] = results[0]
        session['password'] = results[1]
        session['user_id'] = results[2]
        session['username'] = results[3]
        # flash('You were successfully logged in')
        return redirect('/user_info')
    
    else:
        
        # ('You information is incorrect, try again')
        return redirect('/')
# ------- logout  ------- #

@app.route('/log_out')
def log_out():
  session.clear()
  return redirect('/')
    
# ------- Sign up ------- #

@app.route('/sign_up', methods=['POST'])
def sign_up():
    
   username = request.form.get('username')
   # put email validator in here 
   email = request.form.get('email')
   # password bcrypterator in here
   password = request.form.get('password')
   hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
   
   conn = psycopg2.connect(DB_URL)
   cur = conn.cursor()
   
   cur.execute('INSERT INTO motus_users (username, email, hash_pw) VALUES(%s, %s, %s)', [username, email, hash_pw])
   conn.commit()
   conn.close()
   return redirect('/user_info')

# ------- Add rides ------- #

@app.route('/add_rides', methods=['GET'])
def add_ride():
    return render_template('add_ride.html')

# ------- processing adding rides ------- #

@app.route('/process_rides', methods=['POST'])
def process_rides():
    user_id = session.get('user_id')
    ride_description = request.form.get('ride_description')
    ride_start = request.form.get('ride_start')
    ride_end = request.form.get('ride_end')
    print(ride_start,ride_end,ride_description)
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    cur.execute('INSERT INTO rides (user_id, ride_description, ride_start, ride_end) VALUES (%s, %s, %s, %s)', [user_id, ride_description, ride_start, ride_end])
    conn.commit()
    conn.close()
    print('i work')
    return redirect('/show_rides')
    
# ------- setting session/cookies ------- #   

@app.route('/user_info')
def method_name():
    username = session.get('username')
    return render_template('user.html', username=username)

# ------- displaying rides from tables ------- #
@app.route('/show_rides')
def show_rides():
    user_id = session.get('user_id')
    username = session.get('username')
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT * FROM rides WHERE user_id = %s', [user_id])
    rides = cur.fetchall()
    print(rides)
    conn.commit()
    conn.close()
    
 
    return render_template('show_rides.html' , KEY=KEY, rides=rides, username=username)

# ------- deleting rides ------- #

@app.route('/delete/<int:ride_id>')
def delete(ride_id):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('DELETE FROM rides WHERE ride_id = %s', [ride_id])
    conn.commit()
    return redirect('/show_rides')

# ------- settings page ------- #

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == "__main__":
    app.run(debug=True)