from flask import Blueprint, render_template, session, redirect, jsonify, request
from .googlepalm import response_AI
import clipboard
from .models import get_data

views = Blueprint('views', __name__)
conversation = []

@views.route('/')
def home():
    if session.get('logged_in') and session.get('username'):
        return redirect('/shri')
    session.clear()
    return render_template("home.html")

# Chatbot Page
@views.route('/shri', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        user_prompt = request.form.get("message")
        if user_prompt == '':
            ai_response = 'No input provided'
        else:
            ai_response = response_AI(user_prompt)     
            conversation.append({'user': user_prompt, 'response': ai_response, 'is_code': True})
    return render_template("shri.html", username= session.get('username'),conversation=conversation)

@views.route('/api')
def api_docs():
    return render_template("apidoc.html")

# API
@views.route('/api/<string:username>/<string:user_prompt>', methods=['GET'])
def api(username, user_prompt):
    existing_user = get_data(
        f"SELECT username FROM Users WHERE username='{username}'")
    if not existing_user:
        return jsonify({'error': 'User does not exist'}), 404
    if user_prompt == ' ':
        ai_response = 'No input provided'
    else:
        user_prompt = user_prompt.replace("%20", " ")
        ai_response = response_AI(user_prompt)
    response = {
        'username': username,
        'user_prompt': user_prompt,
        'response': ai_response,
    }
    return jsonify(response)

# Clear Chatbot
@views.route('/clear')
def clear():
    conversation.clear()
    return redirect('/shri')

@views.route('/copy')
def copy():
    clipboard.copy(conversation[-1]['response'])
    return redirect('/shri')