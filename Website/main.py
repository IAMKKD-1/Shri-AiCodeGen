from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import os
import mysql.connector
import bcrypt
from responses import generate_responses
from otpsender import send_otp_email

host=os.getenv('HOST')
user=os.getenv('USER')
password=os.getenv('PASSWD')
database=os.getenv('DBNAME')

app = Flask(__name__)
app.secret_key = os.urandom(24)

try:
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
                return render_template('home.html', username=session['username'][:10], conversation=conversation)
        else:
            return redirect('/')
        
    @app.route('/logout')
    def logout():
        conversation.clear()
        session.pop('username')
        return redirect('/')

    @app.route('/clear')
    def clear():
        conversation.clear()
        return redirect('/home')

    @app.route('/api/<string:user_prompt>', methods=['GET'])
    def api(user_prompt):
        if user_prompt == '':
            return jsonify({'user_prompt': user_prompt, 'response': 'No input provided'})
        response = {
            'user_prompt': user_prompt,
            'response': generate_responses(user_prompt)[0],
        }
        return jsonify(response)
    
    @app.route('/api')
    def api_home():
        return render_template('api-doc.html')
    
    @app.route('/forgot-password', methods=['GET', 'POST'])
    def forgot_password():
        reset_email = session.get('reset_email')
        
        if reset_email:
            if request.method == 'POST':
                otp = request.form.get('otp')
                password = request.form.get('password')
                confirm_password = request.form.get('confirm_password')

                if otp:
                    if otp == session.get('otp'):
                        if password != confirm_password:
                            return render_template('forgot-password.html', message='Passwords do not match')
                        
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                        cursor.execute("UPDATE users SET password_hash = %s WHERE email = %s", (hashed_password, reset_email))
                        conn.commit()
                        session.pop('reset_email')
                        return redirect('/login') 
                    else:
                        return render_template('forgot-password.html', message='Invalid OTP', reset_email=reset_email)
            else:
                return render_template('forgot-password.html', reset_email=reset_email)

        if request.method == 'POST':
            email = request.form.get('email')
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user:
                session['reset_email'] = email
                session['otp'] = send_otp_email(email)
                return render_template('forgot-password.html', reset_email=session['reset_email'])
            else:
                return render_template('forgot-password.html', message='Invalid email')
        
        return render_template('forgot-password.html')


    @app.route('/resend-otp')
    def resend_otp():
        email = session.get('reset_email')
        if not email:
            return redirect('/forgot-password')
        session['otp'] = send_otp_email(email)
        return redirect('/forgot-password')
    

except Exception:
    print("Error connecting to database")

if __name__ == "__main__":
    app.run(debug=True)
    cursor.close()
    conn.close()
