import os
import time
import random
import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, send
import sys

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=os.environ['PORT'])