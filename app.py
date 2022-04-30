from flask import Flask, request,  redirect, render_template, session
import os 
import psycopg2

DB_URL = os.environ.get('DATABASE_URL','dbname=motus')
SECRET_KEY = os.environ.get('SECRET_KEY', 'pretend secret  KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/login', methods=['POST'])
def login_action():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT id, email, name FROM motus_users WHERE email = %s", [email])
    results = cur.fetchone()
     
    conn.commit()
    conn.close()
    # If not, redirect back to the login page.
    if results != None:
    # If valid - set the user ID in session and redirect
        session['id'] = results[0]
        session['email'] = results[1]
        session['name'] = results[2]
        return render_template('login.html')
    else:
        return render_template('login.html')
    
@app.route('/signup', methods=['POST'])
def sign_up():
   username = request.form.get('username')
   email = request.form.get('email')
   password = request.form.get('password')
   
   conn = psycopg2.connect(DB_URL)
   cur = conn.cursor()
   cur.execute('INSERT INTO motus_users (username, email, password) VALUES(%s, %s, %s)', [username, email, password])
   conn.commit()
   return render_template('add_ride.html')
   
if __name__ == "__main__":
    app.run(debug=True)