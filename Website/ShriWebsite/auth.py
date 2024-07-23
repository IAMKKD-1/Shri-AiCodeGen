from flask import Blueprint, render_template, request, redirect, session
import bcrypt
from .models import insert_data, update_data, get_data
from .otp import send_otp_email
from .views import conversation

auth = Blueprint('auth', __name__)

# SignUp
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if session.get('logged_in') and session.get('username'):
        return redirect('/')
    email = session.get('email')
    if email:
        if request.method == 'POST':
            entered_otp = request.form.get('otp')
            if session.get('otp') == entered_otp:
                username = session.get('username')
                email = session.get('email')
                password = request.form.get('password')
                confirm_password = request.form.get('confirm-password')

                if password == confirm_password:
                    if len(password) < 8:
                        return render_template("signup.html", email=email, error_message="Password must be at least 8 characters")
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    hashed_password = hashed_password.decode('utf-8')
                    
                    insert_query = "INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)"
                    data = (username, email, hashed_password)
                    insert_data(insert_query=insert_query, data=data)
                    session.pop('email')
                    session.pop('otp')
                    session['logged_in'] = True
                    return redirect('/shri')
                else:
                    return render_template("signup.html", email=email, error_message="Passwords do not match")
            else:
                return render_template("signup.html", email=email, error_message="Incorrect OTP")

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')

        existing_user = get_data(
            f"SELECT * FROM Users WHERE username='{username}' OR email='{email}'")
        if existing_user:
            if existing_user[0][1] == username or existing_user[0][2] == email:
                return render_template("signup.html", error_message="Username or Email already exists")
        otp = send_otp_email(email)
        session['username'] = username
        session['email'] = email
        session['otp'] = otp
        return render_template("signup.html", email=email)
    if email:
        return render_template("signup.html", email=email)
    else:
        return render_template("signup.html")

# Login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in') and session.get('username'):
        return redirect('/')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = get_data(
            f"SELECT * FROM Users WHERE username='{username}' or email='{username}'")
        if existing_user:
            if existing_user[0][1] == username or existing_user[0][2] == username:
                stored_hashed_password = existing_user[0][3]
                if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                    session['username'] = existing_user[0][1]
                    session['logged_in'] = True
                    return redirect('/shri')
                else:
                    return render_template("login.html", error_message="Incorrect Password")
        else:
            return render_template("login.html", error_message="Username doesn't exist. Please Signup!")
    return render_template("login.html")

# Logout
@auth.route('/logout')
def logout():
    session.clear()
    conversation.clear()
    return redirect('/')

# Reset Password
@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    reset_email = session.get('reset_email')
    if reset_email:
        if request.method == 'POST':
            entered_otp = request.form.get('otp')
            stored_otp = session.get('otp')
            if stored_otp and stored_otp == entered_otp:
                password = request.form.get('password')
                confirm_password = request.form.get('confirm-password')

                if password == confirm_password:
                    if len(password) < 8:
                        return render_template("resetpass.html", reset_email=reset_email,  error_message="Password must be at least 8 characters")
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    update_query = "UPDATE Users SET password = %s WHERE email = %s"
                    data = (hashed_password, reset_email)
                    update_data(update_query=update_query, data=data)
                    session.pop('reset_email')
                    session.pop('otp')
                    return redirect('/auth/login')
                else:
                    return render_template("resetpass.html", reset_email=reset_email, error_message="Passwords do not match")
            else:
                return render_template("resetpass.html", reset_email=reset_email, error_message="Incorrect OTP")

    if request.method == 'POST':
        reset_email = request.form.get('reset-email')
        user_data = get_data(f"SELECT * FROM Users WHERE email='{reset_email}'")
        if user_data:
            session['reset_email'] = reset_email
            session['otp'] = send_otp_email(reset_email)
            return render_template('resetpass.html', reset_email=reset_email)
        else:
            return render_template('resetpass.html', error_message='Invalid email')
    if reset_email:
        return render_template("resetpass.html", reset_email=reset_email)
    else:
        return render_template('resetpass.html')

# Resend OTP for Signup
@auth.route('/resend-otp-signup')
def resend_otp_signup():
    email = session.get('email')
    session['otp'] = send_otp_email(email)
    return redirect('/auth/signup')

# Resend OTP for Reset Password
@auth.route('/resend-otp-resetpass')
def resend_otp_resetpass():
    reset_email = session.get('reset_email')
    session['otp'] = send_otp_email(reset_email)
    return redirect('/auth/reset-password')

# Change Email
@auth.route('/change-email')
def change_email():
    session.pop('reset_email')
    return redirect('/auth/reset-password')