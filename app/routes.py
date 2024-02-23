# /app/routes.py
from app import app, socketio
from flask import render_template, request, redirect, url_for, session
from flask_socketio import emit
import os

import logging

users = {}

import secrets

secret_key = secrets.token_hex(16)
app.secret_key = secret_key


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        starsign = request.form['starsign']
        users[username] = starsign
        starsign_image_url = get_starsign_image_url(starsign)
        return redirect(url_for('chatroom', username=username, starsign=starsign, starsign_image_url=starsign_image_url))
    return render_template('index.html')

@app.route('/chatroom')
def chatroom():
    current_user = request.args.get('username')
    current_starsign = request.args.get('starsign')
    starsign_image_url = request.args.get('starsign_image_url')

    if current_user is None or current_starsign is None:
        return "Error: No username or starsign provided."

    same_starsign_users = {username: sign for username, sign in users.items() if sign == current_starsign}

    return render_template('chatroom.html', current_user=current_user, current_starsign=current_starsign,
                           starsign_image_url=starsign_image_url, users=same_starsign_users)

@socketio.on('connect')
def handle_connect():
    print('Client connected:', request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected:', request.sid)

@socketio.on('audio')
def handle_audio(audio_data):
    try:
        # print('Audio data received from client:', audio_data)
        # Process the audio data here
        # Broadcast audio data to all clients in the same room
        sender = session.get('username')  # Assuming you store the username in the session
        emit('audio', {'audio': audio_data, 'sender': sender}, broadcast=True)
        print('Session data:', session)
        print(sender)
        logging.info('Broadcasted audio data to all clients.')
    except Exception as e:
        print('Error processing audio data:', str(e))
        logging.error('Error processing audio data:', exc_info=True)

def get_starsign_image_url(starsign):
    # Replace this with your logic to get the star sign image URL based on the starsign
    # Example:
    image_urls = {
        'Aries': 'https://imgs.search.brave.com/AM_5nYenkuiusEJaKd5fccvn1BMHjCWaGvyjLa0dRSY/rs:fit:860:0:0/g:ce/aHR0cHM6Ly9oaXBz/LmhlYXJzdGFwcHMu/Y29tL2htZy1wcm9k/L2ltYWdlcy9hcmll/cy1maW5hbC02NWM1/M2EzOTFjNmVkLmpw/Zz9jcm9wPTF4dzox/eGg7Y2VudGVyLHRv/cCZyZXNpemU9NjQw/Oio',
        'Taurus': 'https://imgs.search.brave.com/eFJcVXKuBKPAcIHuqO80UqcQdI9mHE6D4t0Iwdk-ug8/rs:fit:860:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvOTcy/MzA5NzEvdmVjdG9y/L3RhdXJ1cy5qcGc_/cz02MTJ4NjEyJnc9/MCZrPTIwJmM9Sk9k/ak1VdjYxQTdKWlpn/WG5YLVJOTk9VdXQw/TWE3aGE0cXpseWdE/REVsYz0',
        'Gemini' : "https://imgs.search.brave.com/LefTrAXyHa6XfepeqaFRt6eLCGjt3YrH9-cQ_Lr4P9s/rs:fit:860:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMTMx/NTg2NzcyL3ZlY3Rv/ci9nZW1pbmkuanBn/P3M9NjEyeDYxMiZ3/PTAmaz0yMCZjPTkz/YTBIYzdyQUxGMXdG/N09PZlRtWDJZdGUy/RllMbFRqcm9vQXc2/VGRHSlE9",
        'Cancer' : "https://imgs.search.brave.com/c7nlFHk-s5RPrOFN_LE32hbivQ4cJB_MsC4w1OXQ6_c/rs:fit:860:0:0/g:ce/aHR0cHM6Ly90NC5m/dGNkbi5uZXQvanBn/LzA0LzUzLzU3LzEx/LzM2MF9GXzQ1MzU3/MTE5NF9MNm9rbmpp/MHk2YXRDeTZ6RzNH/allFeWt6N0x6Y2h4/Yi5qcGc",
        'Leo': "https://imgs.search.brave.com/1xCpCun6MDSGzYIUCUDJz9xlRuYiP5NAlcB6diYiBmg/rs:fit:860:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMTIw/NjMxMTM2NS9waG90/by9sZW8uanBnP3M9/NjEyeDYxMiZ3PTAm/az0yMCZjPVlObkNy/a0l1OXp6T0czV0ht/NEN4eFhvekVqUlZV/ampPbkZnYU1pSHhI/YzQ9",
        # Add more star sign image URLs as needed
    }
    return image_urls.get(starsign, '')
