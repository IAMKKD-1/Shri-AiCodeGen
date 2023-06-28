from flask import Flask, render_template, request, redirect, session, url_for
import os
import mysql.connector
from dotenv import load_dotenv
import bcrypt
from responses import generate_responses
from pygments.formatters import HtmlFormatter

load_dotenv()
host=os.getenv('HOST')
user=os.getenv('USER')
password=os.getenv('PASSWD')
database=os.getenv('DBNAME')

app = Flask(__name__)
app.secret_key = os.urandom(24)

conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
cursor = conn.cursor()

conversation = []

@app.route('/')
def index():
    if 'username' in session:
        return redirect('/home')
    else:
        return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        if password != confirm_password:
            error_message = "Passwords do not match"
            return render_template('signup.html', error_message=error_message)

        cursor.execute(f"SELECT * FROM users WHERE username = '{username}' or email = '{email}'")
        if cursor.fetchone():
            return render_template('signup.html', error_message='Username/Email already exists')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        insert_query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (username, email, hashed_password))
        conn.commit()

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['username'] = username
            return redirect('/home')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/home')
    else:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
                session['username'] = username
                return redirect('/home')
            else:
                return render_template('login.html', error_message='Invalid username/password')

        return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' in session:
        if request.method == 'POST':
            message = request.form.get('message')
            response, code = generate_responses(message)
            conversation.append({'user': message, 'response': response, 'is_code': code})
            return redirect(url_for('home'))  
        else:
            return render_template('home.html', username=session['username'][:10], conversation=conversation, pygments_css = HtmlFormatter().get_style_defs('.highlight'))
    else:
        return redirect('/login')
    
@app.route('/logout')
def logout():
    conversation.clear()
    session.pop('username')
    return redirect('/')

@app.route('/clear')
def clear():
    conversation.clear()
    return redirect('/home')


if __name__ == "__main__":
    app.run(debug=True)
    cursor.close()
    conn.close()