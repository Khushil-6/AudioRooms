from flask import Flask
from flask_socketio import SocketIO
import os


app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)

from app import routes
