import os
import time
import random
import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import sys
from Game import Game

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

games = {}

@socketio.on('join')
def onJoin(data):
    data = json.loads(data)
    roomCode = data["roomCode"]
    games[roomCode].addPlayer(False, request.sid)
    for p in games[roomCode].players:
        player = games[roomCode].players[p]
        emit('lobbyData', games[roomCode].getLobbyDataJSON(player.sessionID), room=player.sessionID)

@socketio.on('create')
def onCreate(data):
    game = Game()
    games[game.roomCode] = game
    game.addPlayer(True, request.sid)
    emit('lobbyData', game.getLobbyDataJSON(request.sid))

@socketio.on('leave')
def onLeave(data):
    print(request.sid, file=sys.stderr)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=os.environ['PORT'])